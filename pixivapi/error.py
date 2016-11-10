from __future__ import print_function

import six

class PixivError(Exception):

    def __init__(self, reason, response=None):
        Exception.__init__(self, reason)
        if six.PY3 or isinstance(reason, six.text_type):
            self.reason = six.text_type(reason)
        elif isinstance(reason, str):
            self.reason = reason.decode('utf-8')
        else:
            raise TypeError

        self.response = response

    def __str__(self):
        if six.PY2:
            return six.text_type(self.reason).encode('utf-8')
        else:
            return self.reason
