from __future__ import print_function

import requests
import six

from .error import PixivError

def convert_to_utf8_str(arg):
    if isinstance(arg, six.text_type):
        arg = arg.encode('utf-8')
    elif not isinstance(arg, bytes):
        arg = six.text_type(arg).encode('utf-8')
    return arg

class PixivDownload(object):

    def __init__(self,
                 headers={'User-Agent': 'PixivIOSApp/6.2.1 (iOS 9.0.2; iPhone6,1)',
                          'Referer': 'https://app-api.pixiv.net/'},
                 timeout=60):

        self.timeout = timeout
        self.headers = headers

    def get(self, url):
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout, stream=True)
        except Exception as e:
            raise PixivError('Failed to send request: %s' % e)

        if resp.status_code and not 200 <= resp.status_code < 300:
            try:
                error_msg = resp.text
            except Exception:
                error_msg = 'PixivAPI error response: status code = %s' % resp.status_code
            raise PixivError(error_msg)

        return resp.content
