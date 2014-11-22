#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pixiv.api import PixivAPI, PixivIllustLookup, PixivIllustSearch, PixivResultParser, PixivNovelSearch, PixivNovelLookup, PixivUserSearch
from config import config, args

def pixiv_bot():
    api = PixivAPI(config.pixiv.user, config.pixiv.passwd)

    # イラストルックアップ
    illust = PixivIllustLookup(api)
    print illust.lookup(47162152)

    # 小説ルックアップ
    novel = PixivNovelLookup(api)
    print novel.lookup(4579009)

    # イラスト検索
    for result in PixivIllustSearch(api, keyword='魔法少女まどか☆マギカ', page=200):
        for illust in PixivResultParser(result):
            print illust
            print 'id: %s title: %s by %s (%s)' % (illust.id, illust.title, illust.display_name, illust.user_name)

    # 小説検索
    for result in PixivNovelSearch(api, keyword='魔法少女まどか☆マギカ', page=200):
        for novel in PixivResultParser(result):
            print novel
            print 'id: %s title: %s by %s (%s)' % (novel.id, novel.title, novel.display_name, novel.user_name)

    # ユーザー検索
    for result in PixivUserSearch(api, keyword='まどか', page=1):
        for user in PixivResultParser(result):
            print user
            print 'id: %s user_name: %s (%s)' % (user.user_id, user.display_name, user.user_name)

if __name__ == '__main__':
    pixiv_bot()
