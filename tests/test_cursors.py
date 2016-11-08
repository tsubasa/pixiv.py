# -*- coding: utf-8 -*-

import unittest
import vcr

from pixivapi import AppPixivAPI, AppCursor

tape = vcr.VCR(
    cassette_library_dir='cassettes',
    filter_headers=['Authorization'],
    serializer='json',
    record_mode='once',
)

class PixivAPITestCase(unittest.TestCase):
    def setUp(self):
        self.api = AppPixivAPI()

class AppCursorTests(PixivAPITestCase):

    @tape.use_cassette('testcursoritems.json')
    def testcursoritems(self):
        items = list(AppCursor(self.api.search_illust, word='original').items(5))
        self.assertEqual(len(items), 5)

    @tape.use_cassette('testcursorpages.json')
    def testcursorpages(self):
        pages = list(AppCursor(self.api.search_illust, word='original').pages(5))
        self.assertEqual(len(pages), 5)
