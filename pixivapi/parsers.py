# -*- coding: utf-8 -*-

from __future__ import print_function

import json as import_simplejson
import re

from .error import PixivError
from .models import ModelFactory, AppModelFactory

re_offset_template = re.compile('offset=(\d+)')

class Parser(object):

    def parse(self, method, payload):
        raise NotImplementedError

    def parse_error(self, payload):
        raise NotImplementedError

class JSONParser(Parser):

    def __init__(self):
        self.json_lib = import_simplejson

    def parse(self, method, payload, pagination):
        try:
            json = self.json_lib.loads(payload)
        except Exception as e:
            raise PixivError('Failed to parse JSON payload: %s' % e)

        cursors = {}
        if pagination and 'pagination' in json:
            cursors.update({'previous': json['pagination'].get('previous', None)})
            cursors.update({'next': json['pagination'].get('next', None)})
            cursors.update({'per_page': json['pagination'].get('per_page', None)})
            cursors.update({'pages': json['pagination'].get('pages', None)})
            cursors.update({'total': json['pagination'].get('total', None)})

        if cursors and isinstance(json, dict):
            return json, cursors
        else:
            return json

    def parse_error(self, payload):
        return self.json_lib.loads(payload)

class ModelParser(JSONParser):

    def __init__(self, model_factory=None):
        JSONParser.__init__(self)
        self.model_factory = model_factory or ModelFactory

    def parse(self, method, payload, pagination=False):
        try:
            if method.payload_type is None:
                return
            model = getattr(self.model_factory, method.payload_type)
        except AttributeError:
            raise PixivError('No model for this payload type: %s' % method.payload_type)

        json = JSONParser.parse(self, method, payload, pagination)
        if isinstance(json, tuple):
            json, cursors = json
        else:
            cursors = None

        if method.payload_list:
            result = model.parse_list(method.api, json['response'])
        else:
            result = model.parse(method.api, json['response'][0])

        if cursors:
            return result, cursors
        else:
            return result

class AppJSONParser(Parser):

    def __init__(self):
        self.json_lib = import_simplejson

    def parse(self, method, payload, pagination):
        try:
            json = self.json_lib.loads(payload)
        except Exception as e:
            raise PixivError('Failed to parse JSON payload: %s' % e)

        cursors = {}
        if pagination and 'next_url' in json and json['next_url']:
            offset = re_offset_template.findall(json['next_url'])
            if offset:
                cursors.update({'offset': offset[0]})

        if cursors and isinstance(json, dict):
            return json, cursors
        else:
            return json

    def parse_error(self, payload):
        return self.json_lib.loads(payload)

class AppModelParser(AppJSONParser):

    def __init__(self, model_factory=None):
        AppJSONParser.__init__(self)
        self.model_factory = model_factory or AppModelFactory

    def parse(self, method, payload, pagination=False):
        try:
            if method.payload_type is None:
                return
            model = getattr(self.model_factory, method.payload_type)
        except AttributeError:
            raise PixivError('No model for this payload type: %s' % method.payload_type)

        json = AppJSONParser.parse(self, method, payload, pagination)
        if isinstance(json, tuple):
            json, cursors = json
        else:
            cursors = None

        if method.payload_list:
            result = model.parse_list(method.api, json)
        else:
            result = model.parse(method.api, json)

        if cursors:
            return result, cursors
        else:
            return result
