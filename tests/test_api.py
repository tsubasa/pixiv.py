from .config import PixivAPITestCase, tape

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

    @tape.use_cassette('testuserbookmarktagsillust.json')
    def testuserbookmarktagsillust(self):
        self.api.user_bookmark_tags_illust(user_id=10)

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

    @tape.use_cassette('testuserrecommended.json')
    def testuserrecommended(self):
        self.api.user_recommended()

    @tape.use_cassette('testillustrecommended.json')
    def testillustrecommended(self):
        self.api.illust_recommended()

    @tape.use_cassette('testmangarecommended.json')
    def testmangarecommended(self):
        self.api.manga_recommended()

    @tape.use_cassette('testnovelrecommended.json')
    def testnovelrecommended(self):
        self.api.novel_recommended()
