#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import csv
import cStringIO
import random

from handlers import RedirectCatchHeader

PIXIV_SP_REFERRER = 'http://spapi.pixiv.net/'

class PixivApi(object):

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
            raise Exception('セッション取得エラー')

    @property
    def login(self):
        return 'https://www.secure.pixiv.net/login.php'

    @property
    def illust(self):
        return ''.join([self.scheme, '://', self.host, '/iphone/illust.php'])

    @property
    def search(self):
        return ''.join([self.scheme, '://', self.host, '/iphone/search.php'])

class PixivIllustLookup(object):

    def __init__(self, api, content='all'):
        if (isinstance(api, PixivApi)):
            self._api = api
            self.content = content
        else:
            raise Exception('PixivApiオブジェクトではありません')

    def lookup(self, illust_id):
        headers = {'User-Agent': self._api.ua,
                   'Cookie': 'PHPSESSID=' + self._api.phpsess}
        values = {'PHPSESSID': self._api.phpsess,
                  'content': self.content,
                  'illust_id': illust_id,
                  }

        request = urllib2.Request('?'.join([self._api.illust, urllib.urlencode(values)]), headers=headers)
        opener = urllib2.build_opener()

        try:
            return opener.open(request).read()
        except:
            raise None

class PixivIllustSearch(object):

    PIXIV_SP_SEARCH_MAX_PAGE = 200

    def __init__(self, api, keyword='', page=1, order='', scd='', mode='s_tag'):
        if (isinstance(api, PixivApi)):
            self._api = api
            self.keyword = keyword
            self.page = page
            self.mode = mode
            self.order = order
            self.scd = scd
        else:
            raise Exception('PixivApiオブジェクトではありません')

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
        :param order: 並び順 [None] 新しい順, [date] 古い順
        """
        self.order = order

    def set_scd(self, scd=''):
        """
        :param scd: 指定日から現在までの投稿期間 [YYYY-MM-DD]
        """
        self.scd = scd

    def set_page(self, page):
        if isinstance(page, int):
            self.page = page
        else:
            raise TypeError('Not Numeric')

    def search(self, keyword=''):
        self.keyword = keyword if keyword else self.keyword

        if self.page > self.PIXIV_SP_SEARCH_MAX_PAGE:
            return None

        headers = {'User-Agent': self._api.ua,
                   'Cookie': 'PHPSESSID=' + self._api.phpsess}
        values = {'PHPSESSID': self._api.phpsess,
                  'word': self.keyword,
                  'p': self.page,
                  's_mode': self.mode,
                  'order': self.order,
                  'scd': self.scd,
                  }

        request = urllib2.Request('?'.join([self._api.search, urllib.urlencode(values)]), headers=headers)
        opener = urllib2.build_opener()

        try:
            return opener.open(request).read()
        except Exception:
            return None

class PixivResultParser(object):

    def __init__(self, data):
        self.rows = list(csv.reader(cStringIO.StringIO(data)))
        if self.rows:
            self.size = len(self.rows)
            self.cursor = 0
        else:
            raise Exception('No data')

    def __iter__(self):
        return self

    def next(self):
        if self.size <= self.cursor:
            raise StopIteration

        try:
            return PixivIllustModel.parse(self.rows[self.cursor])
        finally:
            self.cursor += 1

class PixivUtils(object):

    @staticmethod
    def abs_img_url(illust_id, user_name, ext, prefix, page, thumb, posted_at, tags):
        img_list = []

        if thumb and 'img-master' in thumb:
            if page:
                # http://i1.pixiv.net/img-original/img/2014/10/01/21/51/02/{illust_id}_p0.jpg
                # http://i1.pixiv.net/img-original/img/2014/10/01/21/51/02/{illust_id}_p1.jpg ...
                for p in range(0, int(page)):
                    img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-original/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(illust_id) + '_p' + str(p) + '.' + ext)
            elif 'うごイラ' in tags:
                img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-zip-ugoira/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(illust_id) + '_ugoira600x600.zip')
            else:
                # http://i2.pixiv.net/img-original/img/2014/10/02/07/46/59/{illust_id}_p0.jpg
                img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-original/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(illust_id) + '_p0' + '.' + ext)

        elif thumb and 'img-inf' in thumb:
            if page:
                for p in range(0, int(page)):
                    img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(illust_id) + '_big_p' + str(p) + '.' + ext)
            else:
                # http://i1.pixiv.net/img{prefix}/img/{user_name}/{illust_id}.jpg
                img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(illust_id) + '.' + ext)

        return img_list

class PixivModel(object):

    @classmethod
    def parse(cls, row):
        raise NotImplementedError

    @classmethod
    def parse_list(cls, rows):
        results = []
        for row in rows:
            if row:
                results.append(cls.parse(row))
        return results

class PixivIllustModel(PixivModel):

    """
    :param row[0]   : illust_id
    :param row[1]   : user_id
    :param row[2]   : extension
    :param row[3]   : image title
    :param row[4]   : image directory prefix
    :param row[5]   : post_name
    :param row[6]   : mobile thumbnail (128x128) /img-inf/ or /img-master/
    :param row[7]   : unused/empty
    :param row[8]   : unused/empty
    :param row[9]   : mobile thumbnail (480mw)
    :param row[10]  : unused/empty
    :param row[11]  : unused/empty
    :param row[12]  : upload date
    :param row[13]  : space-delimited list of tags
    :param row[14]  : drawing software (e.g. SAI)
    :param row[15]  : number of ratings
    :param row[16]  : total score (sum of all ratings)
    :param row[17]  : number of views
    :param row[18]  : image description (raw HTML)
    :param row[19]  : number of pages (empty if not a manga sequence)
    :param row[20]  : unused/empty
    :param row[21]  : unused/empty
    :param row[22]  : number of favorites
    :param row[23]  : number of comments
    :param row[24]  : artist username
    :param row[25]  : unused/empty
    :param row[26]  : R-18 marker (0 is safe, 1 is R-18, 2 is R-18G)
    :param row[27]  : novel series id (blank for illustrations and novels not part of a series)
    :param row[28]  : unused/empty
    :param row[29]  : mobile profile image
    :param row[30]  : unused/empty
    """
    # @see https://danbooru.donmai.us/wiki_pages/58938#Explanation of result fields for works

    @classmethod
    def parse(cls, row):
        setattr(cls, 'illust_id', row[0])
        setattr(cls, 'user_id', row[1])
        setattr(cls, 'user_name', row[24])
        setattr(cls, 'title', row[3])
        setattr(cls, 'description', row[18])
        setattr(cls, 'post_name', row[5])
        setattr(cls, 'posted_at', row[12])
        setattr(cls, 'thumb', row[6])
        setattr(cls, 'extension', row[2])
        setattr(cls, 'prefix', row[4])
        setattr(cls, 'tool', row[14])
        setattr(cls, 'page', row[19])
        setattr(cls, 'preview', row[17])
        setattr(cls, 'score', row[16])
        setattr(cls, 'reviewer', row[15])
        setattr(cls, 'bookmark', row[22])
        setattr(cls, 'r18', row[26])
        setattr(cls, 'tags', row[13].split())
        setattr(cls, 'imgs', PixivUtils.abs_img_url(row[0], row[24], row[2], row[4], row[19], row[6], row[12], row[13]))
        return cls
