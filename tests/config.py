import datetime
import os
import unittest
import vcr

from pixiv import AppPixivAPI, OAuthHandler

PIXIV_ACCESS_TOKEN = os.environ.get('PIXIV_ACCESS_TOKEN', None)

tape = vcr.VCR(
    cassette_library_dir='cassettes',
    filter_headers=['Authorization'],
    serializer='json',
    record_mode='once',
)

class PixivAPITestCase(unittest.TestCase):
    def setUp(self):
        self.auth = create_auth()
        self.api = AppPixivAPI(self.auth)

def create_auth():
    auth = OAuthHandler()
    auth.set_token(PIXIV_ACCESS_TOKEN)
    auth.expires = int(datetime.datetime.now().strftime('%s')) + 3600
    return auth
