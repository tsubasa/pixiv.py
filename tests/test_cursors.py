from .config import PixivAPITestCase, tape

from pixivapi import AppCursor

class AppCursorTests(PixivAPITestCase):

    @tape.use_cassette('testcursoritems.json')
    def testcursoritems(self):
        items = list(AppCursor(self.api.search_illust, word='original').items(5))
        self.assertEqual(len(items), 5)

    @tape.use_cassette('testcursorpages.json')
    def testcursorpages(self):
        pages = list(AppCursor(self.api.search_illust, word='original').pages(5))
        self.assertEqual(len(pages), 5)
