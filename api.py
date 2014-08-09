#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import csv
import cStringIO
import random

from handlers import RedirectCatchHeader

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'

PIXIV_LOGIN_URL = 'https://www.secure.pixiv.net/login.php'
PIXIV_SEARCH_URL = 'http://spapi.pixiv.net/iphone/search.php'
PIXIV_SP_REFERRER = 'http://spapi.pixiv.net/'
PIXIV_SP_SEARCH_MAX_PAGE = 200

class PixivApi(object):

    def __init__(self, user, passwd):
        self.phpsess = self.login(user, passwd)

    def login(self, user, passwd):
        headers = {'User-Agent': USER_AGENT}
        values = {'mode': 'login',
                  'pass': passwd,
                  'pixiv_id': user,
                  'skip': '1',
                  }

        request = urllib2.Request(PIXIV_LOGIN_URL, urllib.urlencode(values), headers=headers)
        opener = urllib2.build_opener(RedirectCatchHeader)
        try:
            response = opener.open(request)
        except urllib2.HTTPError as e:
            headers = e.info()

        try:
            return re.findall('PHPSESSID=(.*?);', headers['Set-Cookie'])[0]
        except:
            raise Exception('Login error')

class PixivSearch:

    def __init__(self, api, keyword='', page=1, mode='s_tag'):
        if (isinstance(api, PixivApi)):
            self.api = api
            self.keyword = keyword
            self.page = page
            self.mode = mode
            self.order = ''
        else:
            raise Exception('The API object given was not valid')

    def set_keyword(self, keyword):
        self.keyword = keyword
        self.page = 1

    def set_order(self, order=''):
        self.order = order

    def set_page(self, page):
        self.page = page

    def search(self, keyword=''):
        if self.page > PIXIV_SP_SEARCH_MAX_PAGE:
            return False

        self.keyword = keyword if keyword else self.keyword

        headers = {'User-Agent': USER_AGENT,
                   'Cookie': 'PHPSESSID=' + self.api.phpsess}
        values = {'PHPSESSID': self.api.phpsess,
                  'word': self.keyword,
                  'p': self.page,
                  's_mode': self.mode,
                  'order' : self.order,
                  }

        request = urllib2.Request(PIXIV_SEARCH_URL + '?' + urllib.urlencode(values), headers=headers)
        opener = urllib2.build_opener()

        try:
            response = opener.open(request)
            return response.read()
        except Exception as e:
            raise Exception(e)

    def next(self):
        self.page += 1
        return self.search()

    def prev(self):
        self.page -= 1
        return self.search()

class PixivResultParser:

    def __init__(self, data):
        self.rows = list(csv.reader(cStringIO.StringIO(data)))
        if self.rows:
            self.size = len(self.rows)
            self.cursor = 0
        else:
            raise Exception('No data')

    def get_row_all(self):
        return self.rows

    def get_row(self):
        row = self.rows[self.cursor]
        self._next()
        return row

    def get_image_url_all(self):
        img_list = []
        for num in range(0, self.size):
            img_list += self.parse_image_url(self.rows[num])
        return img_list

    def get_image_url(self):
        row = self.rows[self.cursor]
        self._next()
        return self.parse_image_url(row)

    def parse_image_url(self, data):
        img_list = []
        if data[19]:
            for page in range(0, int(data[19])):
                img_list.append('http://i' + str(random.randint(1,2)) + '.pixiv.net/img' + data[4] + '/img/' + data[24] + '/' + data[0] + '_big_p' + str(page) + '.' + data[2])
        else:
            img_list.append('http://i' + str(random.randint(1,2)) + '.pixiv.net/img' + data[4] + '/img/' + data[24] + '/' + data[0] + '.' + data[2])
        return img_list

    def _next(self):
        if self.cursor < self.size:
            self.cursor += 1

    def _prev(self):
        if self.cursor:
            self.cursor -= 1
