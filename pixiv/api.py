#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import csv
import cStringIO

from error import PixivError
from handlers import RedirectCatchHeader
from models import PixivUserModel, PixivIllustModel, PixivNovelModel

PIXIV_SP_REFERRER = 'http://spapi.pixiv.net/'

class PixivAPI(object):

    def __init__(self, user, passwd, scheme='http', host='spapi.pixiv.net',
                 ua='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'):
        self.scheme = scheme
        self.host = host
        self.ua = ua
        self.phpsess = self._login(user, passwd)

    def _login(self, user, passwd):
        headers = {'User-Agent': self.ua}
        values = {'mode': 'login',
                  'pass': passwd,
                  'pixiv_id': user,
                  'skip': '1',
                  }

        request = urllib2.Request(self.login, urllib.urlencode(values), headers=headers)
        opener = urllib2.build_opener(RedirectCatchHeader)
        try:
            opener.open(request)
        except urllib2.HTTPError as e:
            headers = e.info()

        try:
            return re.findall('PHPSESSID=(.*?);', headers['Set-Cookie'])[0]
        except:
            raise PixivError('ログインに失敗しました')

    @property
    def login(self):
        return 'https://www.secure.pixiv.net/login.php'

    @property
    def illust(self):
        return ''.join([self.scheme, '://', self.host, '/iphone/illust.php'])

    @property
    def novel(self):
        return ''.join([self.scheme, '://', self.host, '/iphone/novel_text.php'])

    @property
    def user(self):
        return ''.join(['https://public-api.secure.pixiv.net/v1/users/{{USER_ID}}.json'])

    @property
    def search_illust(self):
        return ''.join([self.scheme, '://', self.host, '/iphone/search.php'])

    @property
    def search_novel(self):
        return ''.join([self.scheme, '://', self.host, '/iphone/search_novel.php'])

    @property
    def search_user(self):
        return ''.join([self.scheme, '://', self.host, '/iphone/search_user.php'])

class PixivLookup(object):

    def __init__(self, api):
        if (isinstance(api, PixivAPI)):
            self._api = api
        else:
            raise PixivError('PixivApiオブジェクトではありません')

    def _lookup(self, api, headers, values):
        request = urllib2.Request('?'.join([api, urllib.urlencode(values)]), headers=headers)
        opener = urllib2.build_opener()

        try:
            return opener.open(request).read()
        except:
            raise None

class PixivIllustLookup(PixivLookup):

    def __init__(self, api, content='all'):
        super(PixivIllustLookup, self).__init__(api)
        self.content = content

    def lookup(self, illust_id):
        headers = {'User-Agent': self._api.ua,
                   'Cookie': 'PHPSESSID=' + self._api.phpsess}
        values = {'PHPSESSID': self._api.phpsess,
                  'content': self.content,
                  'illust_id': illust_id,
                  }

        return self._lookup(self._api.illust, headers, values)

class PixivNovelLookup(PixivLookup):

    def __init__(self, api):
        super(PixivNovelLookup, self).__init__(api)

    def lookup(self, novel_id):
        headers = {'User-Agent': self._api.ua,
                   'Cookie': 'PHPSESSID=' + self._api.phpsess}
        values = {'PHPSESSID': self._api.phpsess,
                  'id': novel_id,
                  }

        return self._lookup(self._api.novel, headers, values)

class PixivSearch(object):

    PIXIV_SP_SEARCH_MAX_PAGE = 200

    def __init__(self, api, keyword='', page=1, order='', mode='s_tag'):
        if (isinstance(api, PixivAPI)):
            self._api = api
            self.keyword = keyword
            self.page = page
            self.mode = mode
            self.order = order
        else:
            raise PixivError('PixivApiオブジェクトではありません')

    def __iter__(self):
        return self

    def next(self):
        if self.page > self.PIXIV_SP_SEARCH_MAX_PAGE:
            raise StopIteration

        try:
            return self.search()
        finally:
            self.page += 1

    def set_keyword(self, keyword):
        self.keyword = keyword
        self.page = 1

    def set_order(self, order=''):
        """
        :param order: 並び順 [None][date_d] 新しい順, [date] 古い順
        """
        self.order = order

    def set_page(self, page):
        if isinstance(page, int):
            self.page = page
        else:
            raise TypeError('Not Numeric')

    def _search(self, api, headers, values):

        if self.page > self.PIXIV_SP_SEARCH_MAX_PAGE:
            return None

        request = urllib2.Request('?'.join([api, urllib.urlencode(values)]), headers=headers)
        opener = urllib2.build_opener()

        try:
            response = opener.open(request).read()
            if response:
                return response
            else:
                self.page = self.PIXIV_SP_SEARCH_MAX_PAGE
                return None

        except Exception:
            return None

class PixivIllustSearch(PixivSearch):

    def __init__(self, api, keyword='', page=1, order='', scd='', mode='s_tag'):
        super(PixivIllustSearch, self).__init__(api, keyword, page, order, mode)
        self.scd = scd

    def set_scd(self, scd=''):
        """
        :param scd: 指定日から現在までの投稿期間 [YYYY-MM-DD]
        """
        self.scd = scd

    def search(self, keyword=''):
        headers = {'User-Agent': self._api.ua,
                   'Cookie': 'PHPSESSID=' + self._api.phpsess}
        values = {'PHPSESSID': self._api.phpsess,
                  'word': keyword if keyword else self.keyword,
                  'p': self.page,
                  's_mode': self.mode,
                  'order': self.order,
                  'scd': self.scd,
                  }

        return self._search(self._api.search_illust, headers, values)

class PixivNovelSearch(PixivSearch):

    def __init__(self, api, keyword='', page=1, order='date_d', scd='', mode='s_tag'):
        super(PixivNovelSearch, self).__init__(api, keyword, page, order, mode)

    def search(self, keyword=''):
        headers = {'User-Agent': self._api.ua,
                   'Cookie': 'PHPSESSID=' + self._api.phpsess}
        values = {'PHPSESSID': self._api.phpsess,
                  'word': keyword if keyword else self.keyword,
                  'p': self.page,
                  's_mode': self.mode,
                  'order': self.order,
                  }

        return self._search(self._api.search_novel, headers, values)

class PixivUserSearch(PixivSearch):

    def __init__(self, api, keyword='', page=1, order=None, mode=None):
        super(PixivUserSearch, self).__init__(api, keyword, page, order, mode)

    def search(self, keyword=''):
        headers = {'User-Agent': self._api.ua,
                   'Cookie': 'PHPSESSID=' + self._api.phpsess}
        values = {'PHPSESSID': self._api.phpsess,
                  'nick': keyword if keyword else self.keyword,
                  'p': self.page,
                  }

        return self._search(self._api.search_user, headers, values)

class PixivResultParser(object):

    def __init__(self, data):
        if data:
            self.rows = list(csv.reader(cStringIO.StringIO(data)))
            self.size = len(self.rows)
            self.cursor = 0

            if not self.rows[0][0]:
                self.format = 'user'
            elif self.rows[0][2] in ['jpg', 'gif', 'png', 'jpeg']:
                self.format = 'illust'
            else:
                self.format = 'novel'

        else:
            self.size = self.cursor = 0

    def __iter__(self):
        return self

    def next(self):
        if self.size <= self.cursor:
            raise StopIteration

        try:
            if self.format in ['user']:
                return PixivUserModel.parse(self.rows[self.cursor])
            elif self.format in ['illust']:
                return PixivIllustModel.parse(self.rows[self.cursor])
            elif self.format in ['novel']:
                return PixivNovelModel.parse(self.rows[self.cursor])
        finally:
            self.cursor += 1
