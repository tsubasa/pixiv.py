# -*- coding: utf-8 -*-

from pixiv.auth import OAuthHandler
from pixiv.api import PixivAPI, AppPixivAPI
from pixiv.cursor import Cursor, AppCursor
from pixiv.utils import PixivDownload

# r18作品を含める場合必須
auth = OAuthHandler()
auth.login('USERNAME', 'PASSWORD')


#
# Pixiv App API
#
aapi = AppPixivAPI(auth)

# ユーザー詳細取得
print(aapi.user_detail(user_id=10))

# 関連イラスト取得
print(aapi.illust_related(illust_id=20))

# イラストコメント取得
print(aapi.illust_comments(illust_id=20))

# うごイラメタデータ取得
print(aapi.ugoira_metadata(illust_id=44298467))

# イラストお気に入り追加
aapi.illust_bookmark_add(illust_id=20)

# イラストお気に入り削除
aapi.illust_bookmark_delete(illust_id=20)

# 小説取得
print(aapi.novel_text(novel_id=129))

# 小説お気に入り追加
aapi.novel_bookmark_add(novel_id=129)

# 小説お気に入り削除
aapi.novel_bookmark_delete(novel_id=129)

# オートコンプリート
print(aapi.search_autocomplete(word='ラブライブ！'))

# イラスト検索
for illust in aapi.search_illust(word='ラブライブ！'):
    print(illust)

# ユーザー検索
for user in aapi.search_user(word='テスト'):
    print(user)
    break

# 小説検索
for novel in aapi.search_novel(word='ラブライブ！'):
    print(novel)
    break

# イラスト単位で取得件数指定
for illust in AppCursor(aapi.search_illust, word='ラブライブ！').items(20):
    print(illust)

# ページ単位で取得件数指定
for page in AppCursor(aapi.search_illust, word='ラブライブ！').pages(5):
    for illust in page:
        print(illust)

# ユーザーのお気に入りイラスト取得
for illust in aapi.user_bookmarks_illust(user_id=10):
    print(illust)
    break

#
# Pixiv Public API (old)
#
api = PixivAPI(auth)

# イラスト詳細取得
print(api.works(20))

# ユーザー情報
print(api.users(10))

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
