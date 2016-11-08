# -*- coding: utf-8 -*-

import unittest
import vcr

from pixivapi import AppPixivAPI

tape = vcr.VCR(
    cassette_library_dir='cassettes',
    filter_headers=['Authorization'],
    serializer='json',
    record_mode='once',
)

class PixivAPITestCase(unittest.TestCase):
    def setUp(self):
        self.api = AppPixivAPI()

class AppPixivAPITests(PixivAPITestCase):

    @tape.use_cassette('testuserdetail.json')
    def testuserdetail(self):
        self.api.user_detail(user_id=10)

    @tape.use_cassette('testuserillusts.json')
    def testuserillusts(self):
        self.api.user_illusts(user_id=10)

    @tape.use_cassette('testuserbookmarksillust.json')
    def testuserbookmarksillust(self):
        self.api.user_bookmarks_illust(user_id=10)

    @tape.use_cassette('testsearchillust.json')
    def testsearchillust(self):
        self.api.search_illust(word='original')

    @tape.use_cassette('testsearchnovel.json')
    def testsearchnovel(self):
        self.api.search_novel(word='original')

    @tape.use_cassette('testsearchuser.json')
    def testsearchuser(self):
        self.api.search_user(word='test')

    @tape.use_cassette('testsearchautocomplete.json')
    def testsearchautocomplete(self):
        self.api.search_autocomplete(word='test')
