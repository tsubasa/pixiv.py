#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import PixivApi, PixivIllustLookup, PixivIllustSearch, PixivResultParser
from config import config, args

def pixiv_bot():
    api = PixivApi(config.pixiv.user, config.pixiv.passwd)

    # イラストルックアップ
    illust = PixivIllustLookup(api)
    print 'raw data'
    print illust.lookup(47162152)
    # raw data

    for illust in PixivResultParser(illust.lookup(47162152)):
        print 'illust lookup'
        test_print(illust)

    # イラスト検索
    for result in PixivIllustSearch(api, keyword=args.keyword, page=args.page):
        for illust in PixivResultParser(result):
            test_print(illust)

def test_print(illust):
    print illust
    print 'id   : %s' % (illust.illust_id,)
    print 'title: %s by %s (%s)' % (illust.title, illust.post_name, illust.user_name)
    print 'tags : %s' % (', '.join(illust.tags),)
    print illust.imgs
    # object data

if __name__ == '__main__':
    pixiv_bot()
