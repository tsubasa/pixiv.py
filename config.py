#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ConfigParser
import argparse

# define

# args
parser = argparse.ArgumentParser(description='Pixivスクリプト')
parser.add_argument('-k', '--keyword', type=str, default='', help='検索キーワード')
parser.add_argument('-p', '--page', type=int, default=1, help='取得開始ページ位置 default:1 [1-200]')
args = parser.parse_args()

# setting
config_path = os.path.abspath(os.path.dirname(__file__)) + '/config/app.cfg'

# class
class Config(object):
    """Config parser is set setattr"""

    def __init__(self, path):
        if os.path.exists(path):
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(path)
        else:
            raise Exception('Config is not found: %s' % path)

        for section in self.config.sections():
            options = lambda: None
            for option in self.config.options(section):
                setattr(options, option, self.config.get(section, option))

            setattr(self, section, options)

    def get(self, section, option):
        return self.config.get(section, option)

    def getint(self, section, option):
        return self.config.getint(section, option)

config = Config(config_path)
