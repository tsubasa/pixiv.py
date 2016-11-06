# -*- coding: utf-8 -*-

from pixivapi.auth import OAuthHandler
from pixivapi.api import PixivAPI, AppPixivAPI
from pixivapi.cursor import Cursor, AppCursor
from pixivapi.utils import PixivDownload

# r18作品を含める場合必須
auth = OAuthHandler()
auth.login('USERNAME', 'PASSWORD')


#
# Pixiv App API
#
aapi = AppPixivAPI(auth)

# ユーザー詳細取得
print(aapi.user_detail(user_id=1))

# 関連イラスト取得
print(aapi.illust_related(illust_id=1))

# イラストコメント取得
print(aapi.illust_comments(illust_id=1))

# うごイラメタデータ取得
print(aapi.ugoira_metadata(illust_id=1))

# オートコンプリート
print(aapi.search_autocomplete(word='ラブライブ！'))

# イラスト検索
for illust in aapi.search_illust(word='ラブライブ！'):
    print(illust)

# イラスト単位で取得件数指定
for illust in AppCursor(aapi.search_illust, word='ラブライブ！').items(20):
    print(illust)

# ページ単位で取得件数指定
for page in AppCursor(aapi.search_illust, word='ラブライブ！').pages(5):
    for illust in page:
        print(illust)


#
# Pixiv Public API (old)
#
api = PixivAPI(auth)

# イラスト詳細取得
print(api.works(1))

# ユーザー情報
print(api.users(1))

# キーワード検索
print(api.search_works(q='ラブライブ！'))

# イラスト単位で取得件数指定
for work in Cursor(api.search_works, q='ラブライブ！').items(20):
    print(work)

# ページ単位で取得件数指定
for page in Cursor(api.search_works, q='ラブライブ！').pages(5):
    for work in page:
        print(work)


#
# Pixiv Illust Download
#
pixvdl = PixivDownload()

for illust in AppCursor(aapi.search_illust, word='ラブライブ！').items(20):
    if illust.type == 'illust' or illust.type == 'manga':
        if illust.meta_pages:
            for page in illust.meta_pages:
                print(page['image_urls']['original'])
                print(type(pixvdl.get(page['image_urls']['original'])))
        else:
            print(illust.meta_single_page['original_image_url'])
            print(type(pixvdl.get(illust.meta_single_page['original_image_url'])))
    elif illust.type == 'ugoira':
        metadata = aapi.ugoira_metadata(illust_id=illust.id)
        print(metadata.ugoira_metadata['zip_urls']['medium'])
        print(type(pixvdl.get(metadata.ugoira_metadata['zip_urls']['medium'])))
    else:
        print('Unknown type: %s' % illust.type)
        print(illust.type)
