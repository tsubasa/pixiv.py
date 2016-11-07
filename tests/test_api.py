# -*- coding: utf-8 -*-

import time
import unittest

from nose import SkipTest

from pixivapi import AppPixivAPI

class AppPixivAPITestCase(unittest.TestCase):
    def setUp(self):
        self.api = AppPixivAPI()

    def tearDown(self):
        time.sleep(1)

class AppPixivAPITests(AppPixivAPITestCase):

    def test(self):
        raise SkipTest()

    def testuserdetail(self):
        self.api.user_detail(user_id=10)

    def testuserillusts(self):
        self.api.user_illusts(user_id=10)

    def testuserbookmarksillust(self):
        self.api.user_bookmarks_illust(user_id=10)

    def testsearchillust(self):
        self.api.search_illust(word='オリジナル')

    def testsearchnovel(self):
        self.api.search_novel(word='オリジナル')

    def testsearchuser(self):
        self.api.search_user(word='テスト')

    def testsearchautocomplete(self):
        self.api.search_autocomplete(word='テスト')
