# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime

import requests

from .error import PixivError

class AuthHandler(object):

    def auth(self, url, headers, parameters):
        raise NotImplementedError

class OAuthHandler(AuthHandler):

    OAUTH_HOST = 'oauth.secure.pixiv.net'
    OAUTH_ROOT = '/auth/'

    CLIENT_ID = 'bYGKuGVw91e0NMfPGp44euvGt59s'
    CLIENT_SECRET = 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK'

    def __init__(self, username=None, password=None, refresh_token=None):
        self.headers = {
            'App-OS': 'ios',
            'App-OS-Version': '9.3.3',
            'App-Version': '6.2.1',
            'User-Agent': 'PixivIOSApp/6.2.1 (iOS 9.0.2; iPhone6,1)',
        }

        self.client_id = self.CLIENT_ID
        self.client_secret = self.CLIENT_SECRET
        self.access_token = None
        self.refresh_token = None
        self.expires = None

    def _get_oauth_url(self, endpoint):
        return 'https://' + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint

    def get_token(self):
        return self.access_token, self.refresh_token

    def set_token(self, access_token=None, refresh_token=None):
        self.access_token, self.refresh_token = access_token, refresh_token

    def is_token_valid(self):
        return True if self.expires and self.expires > int(datetime.datetime.now().strftime('%s')) else False

    def login(self, username, password):

        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
        }

        return self.auth(url=self._get_oauth_url('token'), parameters=data)

    def refresh(self):

        if not self.refresh_token:
            raise PixivError('refresh_tokenが見つかりません')

        headers = {'Authorization': 'Bearer %s' % self.access_token}

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }

        return self.auth(url=self._get_oauth_url('token'), headers=headers, parameters=data)

    def auth(self, url, headers={}, parameters={}):

        if isinstance(headers, dict):
            headers.update(self.headers)

        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'get_secure_url': 1,
        }

        if isinstance(parameters, dict):
            data.update(parameters)

        try:
            resp = requests.post(url=url, headers=headers, data=data)
        except Exception as e:
            raise PixivError('リクエストエラーが発生しました: %s' % e)

        if resp.status_code and not 200 <= resp.status_code < 300:
            try:
                error_msg = resp.json()['errors']
            except Exception:
                error_msg = 'レスポンスエラーが発生しました: status code = %s' % resp.status_code
            raise PixivError(error_msg)

        data = resp.json()['response']
        if data.get('token_type') != 'bearer':
            raise PixivError('トークンタイプがbearerではありません: %s' % data.get('token_type'))

        for cookie in resp.cookies:
            if cookie.name == 'PHPSESSID':
                self.expires = cookie.expires
                break

        self.access_token = data.get('access_token', None)
        self.refresh_token = data.get('refresh_token', None)

        return self.access_token, self.refresh_token
