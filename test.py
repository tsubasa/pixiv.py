#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import PixivApi, PixivIllustLookup, PixivIllustSearch, PixivResultParser
from config import config, args

def pixiv_bot():
    api = PixivApi(config.pixiv.user, config.pixiv.passwd)

    # イラストルックアップ
    illust = PixivIllustLookup(api)
    print illust.lookup(47162152)
    # raw data

    for illust in PixivResultParser(illust.lookup(47162152)):
        print illust
        print illust.illust_id, illust.title, illust.post_name
        print illust.tags, illust.imgs
        # object data

    # イラスト検索
    for result in PixivIllustSearch(api, keyword=args.keyword, page=args.page):
        for illust in PixivResultParser(result):
            print illust
            print illust.illust_id, illust.title, illust.post_name
            print illust.tags, illust.imgs
            # object data

if __name__ == '__main__':
    pixiv_bot()
