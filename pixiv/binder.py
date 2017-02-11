# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import re

import requests
from six.moves.urllib.parse import quote

from .error import PixivError
from .utils import convert_to_utf8_str

logger = logging.getLogger('pixivapi.binder')

re_path_template = re.compile('{\w+}')

def bind_api(**config):

    class APIMethod(object):

        api = config['api']
        api_root = config.get('api_root', None)
        path = config['path']
        payload_type = config.get('payload_type', None)
        payload_list = config.get('payload_list', False)
        require_auth = config.get('require_auth', False)
        allowed_param = config.get('allowed_param', [])
        require_param = config.get('require_param', [])
        default_param = config.get('default_param', {})
        method = config.get('method', 'GET')
        session = requests.Session()

        def __init__(self, args, kwargs):
            api = self.api

            if self.require_auth and not api.access_token:
                raise PixivError('ログイン認証が必要です')
            elif self.require_auth:
                if not api.auth.is_token_valid():
                    api.refresh_token()

            self.host = api.host
            if not self.api_root:
                self.api_root = api.api_root

            self.parser = kwargs.pop('parser', api.parser)
            self.pagination = kwargs.pop('pagination', False)

            self.session.headers = api.headers
            self.session.headers['Host'] = self.host
            if api.access_token:
                self.session.headers['Authorization'] = 'Bearer %s' % api.access_token

            self.build_parameters(args, kwargs)
            self.build_path()

        def build_parameters(self, args, kwargs):
            self.session.params = {}
            for idx, arg in enumerate(args):
                if arg is None:
                    continue
                try:
                    self.session.params[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise PixivError('パラメータが多すぎます')

            for k, v in self.default_param.items():
                if v is None:
                    continue

                self.session.params[k] = convert_to_utf8_str(v)

            for k, v in kwargs.items():
                if v is None:
                    continue
                if k not in self.allowed_param:
                    raise PixivError('このパラメータは指定できません: %s' % k)

                self.session.params[k] = convert_to_utf8_str(v)

            for k in self.require_param:
                if k not in self.session.params:
                    raise PixivError('パラメータが不足しています: %s' % k)

            logger.info('PARAMS: %r', self.session.params)

        def build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                try:
                    value = quote(self.session.params[name])
                except KeyError:
                    raise PixivError('パラメータが見つかりません: %s' % name)
                del self.session.params[name]

                self.path = self.path.replace(variable, value)

        def execute(self):
            full_url = 'https://' + self.host + self.api_root + self.path

            try:
                if self.method == 'POST':
                    resp = self.session.request(self.method,
                                                full_url,
                                                data=self.session.params,
                                                timeout=self.api.timeout)
                else:
                    resp = self.session.request(self.method,
                                                full_url,
                                                timeout=self.api.timeout)
            except Exception as e:
                raise PixivError('リクエストエラーが発生しました: %s' % e)

            if resp.status_code and not 200 <= resp.status_code < 300:
                try:
                    error_msg = self.parser.parse_error(resp.text)
                except Exception:
                    error_msg = 'レスポンスエラーが発生しました: status code = %s' % resp.status_code
                raise PixivError(error_msg)

            if self.pagination:
                return self.parser.parse(self, resp.text, self.pagination)
            else:
                return self.parser.parse(self, resp.text)

    def _call(*args, **kwargs):
        return APIMethod(args, kwargs).execute()

    return _call
