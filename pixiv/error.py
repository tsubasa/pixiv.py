# -*- coding: utf-8 -*-

class PixivError(Exception):
    """Pixiv API exception"""

    def __init__(self, reason, response=None):
        self.reason = reason
        self.response = response
        Exception.__init__(self, reason)

    def __str__(self):
        return self.reason
