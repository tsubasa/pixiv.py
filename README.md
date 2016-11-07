PixivAPI
=========

[![Build Status](https://travis-ci.org/twopon/PixivAPI.svg?branch=master)](https://travis-ci.org/twopon/PixivAPI)

PixivAPIライブラリ

主な機能
--------

- イラスト検索
- イラスト情報取得
- イラストお気に入り追加/解除
- ユーザー検索
- ユーザー情報取得
- ユーザーフォロー/フォロー解除
- ユーザーお気に入り取得/削除
- 小説検索

TODO
----

- お気に入りタグ取得 (user/bookmark-tags)
- 小説詳細取得 (novel/text)
- 小説シリーズ取得 (novel/series)
- 小説お気に入り追加/解除  (novel/add, novel/delete)

サンプルコード
--------------

```
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

# オートコンプリート
print(aapi.search_autocomplete(word='ラブライブ！'))

# イラスト検索
for illust in aapi.search_illust(word='ラブライブ！'):
    print(illust)

# イラスト検索（イラスト単位で取得件数指定）
for illust in AppCursor(aapi.search_illust, word='ラブライブ！').items(20):
    print(illust)

# イラスト検索（ページ単位で取得件数指定）
for page in AppCursor(aapi.search_illust, word='ラブライブ！').pages(5):
    for illust in page:
        print(illust)

# ユーザー検索
for user in aapi.search_user(word='テスト'):
    print(user)

# 小説検索
for novel in aapi.search_novel(word='ラブライブ！'):
    print(novel)


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
```
