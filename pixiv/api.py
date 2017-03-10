# -*- coding: utf-8 -*-

from __future__ import print_function

from .auth import OAuthHandler
from .binder import bind_api
from .parsers import Parser, ModelParser, AppModelParser

class API(object):
    """Pixiv Base API"""

    access_token = None
    refresh_token = None

    def __init__(self, auth_handler=None):

        self.auth = auth_handler or OAuthHandler()
        self.access_token, self.refresh_token = self.auth.get_token()

    def login(self, username, password):
        self.access_token, self.refresh_token = self.auth.login(username, password)

    def refresh_token(self, refresh_token):
        self.access_token, self.refresh_token = self.auth.refresh_token(refresh_token=self.refresh_token)

class PixivAPI(API):
    """Pixiv Public API"""

    def __init__(self, auth_handler=None, host='public-api.secure.pixiv.net', api_root='/v1', timeout=60, parser=None):
        API.__init__(self, auth_handler)

        self.host = host
        self.api_root = api_root
        self.timeout = timeout
        self.parser = parser or ModelParser()

        self.headers = {'Referer': 'http://spapi.pixiv.net/',
                        'User-Agent': 'PixivIOSApp/5.8.7',
                        }

        if not isinstance(self.parser, Parser):
            raise TypeError('Parserオブジェクトのインスタンスが異なります')

    @property
    def works(self):
        u""" イラスト詳細
        :param id: イラストID
        """
        return bind_api(
            api=self,
            path='/works/{id}.json',
            payload_type='work',
            payload_list=False,
            allowed_param=['id', 'image_sizes', 'include_stats'],
            require_param=['id'],
            default_param={
                'image_sizes': 'px_128x128,small,medium,large,px_480mw',
                'include_stats': True
            }
        )

    @property
    def users(self):
        u""" ユーザー詳細
        :param id: ユーザーID
        """
        return bind_api(
            api=self,
            path='/users/{id}.json',
            payload_type='user',
            payload_list=False,
            allowed_param=['id', 'image_sizes', 'include_stats', 'include_profile', 'include_workspace', 'include_contacts', 'profile_image_sizes'],
            require_param=['id'],
            default_param={
                'image_sizes': 'px_128x128,small,medium,large,px_480mw',
                'include_stats': True,
                'include_profile': True,
                'include_workspace': True,
                'include_contacts': True,
                'profile_image_sizes': 'px_170x170,px_50x50',
            }
        )

    @property
    def search_works(self):
        u""" 作品検索
        :param q: 検索キーワード
        """
        return bind_api(
            api=self,
            path='/search/works.json',
            payload_type='work',
            payload_list=True,
            allowed_param=['q', 'image_sizes', 'include_stats', 'include_sanity_level', 'mode', 'order', 'page', 'per_page', 'period', 'sort', 'types'],
            require_param=['q'],
            default_param={
                'image_sizes': 'px_128x128,large,px_480mw',
                'include_stats': True,
                'include_sanity_level': True,
                'mode': 'text',
                'order': 'desc',
                'page': 1,
                'per_page': 30,
                'period': 'all',
                'sort': 'date',
                'types': 'illustration,manga,ugoira',
            }
        )

class AppPixivAPI(API):
    """Pixiv APP API"""

    def __init__(self, auth_handler=None, host='app-api.pixiv.net', api_root='/v1', timeout=60, parser=None):
        API.__init__(self, auth_handler)

        self.host = host
        self.api_root = api_root
        self.timeout = timeout
        self.parser = parser or AppModelParser()

        self.headers = {'User-Agent': 'PixivIOSApp/6.2.1 (iOS 9.0.2; iPhone6,1)'}

        if not isinstance(self.parser, Parser):
            raise TypeError('Parserオブジェクトのインスタンスが異なります')

    @property
    def user_detail(self):
        u""" ユーザー詳細
        :param user_id: ユーザーID
        """
        return bind_api(
            api=self,
            path='/user/detail',
            payload_type='app_user',
            payload_list=False,
            allowed_param=['user_id'],
            require_param=['user_id'],
            default_param={
                'user_id': self.auth.user_id,
            }
        )

    @property
    def user_illusts(self):
        u""" ユーザーイラスト
        :param user_id: ユーザーID
        :param type: イラストタイプ [illust, manga, ugoira]
        """
        return bind_api(
            api=self,
            path='/user/illusts',
            payload_type='app_illust',
            payload_list=True,
            allowed_param=['user_id', 'filter', 'type'],
            require_param=['user_id'],
            default_param={
                'user_id': self.auth.user_id,
                'filter': 'for_ios',
            }
        )

    @property
    def user_bookmarks_illust(self):
        u""" ユーザーのお気に入りイラスト
        :param user_id: ユーザーID
        :param restrict: 公開／非公開 [public, private]
        """
        return bind_api(
            api=self,
            path='/user/bookmarks/illust',
            payload_type='app_illust',
            payload_list=True,
            allowed_param=['user_id', 'restrict', 'offset', 'page'],
            require_param=['user_id', 'restrict'],
            default_param={
                'user_id': self.auth.user_id,
                'restrict': 'public'
            }
        )

    @property
    def user_bookmark_tags_illust(self):
        u""" ユーザーのお気に入りイラストタグ
        :param user_id: ユーザーID
        :param restrict: 公開／非公開 [public, private]
        """
        return bind_api(
            api=self,
            path='/user/bookmark-tags/illust',
            payload_type='app_tag',
            payload_list=True,
            allowed_param=['user_id', 'restrict', 'offset', 'page'],
            require_param=['user_id', 'restrict'],
            default_param={
                'user_id': self.auth.user_id,
                'restrict': 'public'
            }
        )

    @property
    def user_follow_add(self):
        u""" ユーザーフォロー
        :param user_id: ユーザーID
        :param restrict: 公開／非公開 [public, private]
        """
        return bind_api(
            api=self,
            method='POST',
            path='/user/follow/add',
            require_auth=True,
            allowed_param=['user_id', 'restrict'],
            require_param=['user_id', 'restrict'],
            default_param={
                'restrict': 'public'
            }
        )

    @property
    def user_follow_delete(self):
        u""" ユーザーフォロー解除
        :param user_id: ユーザーID
        """
        return bind_api(
            api=self,
            method='POST',
            path='/user/follow/delete',
            require_auth=True,
            allowed_param=['user_id'],
            require_param=['user_id'],
            default_param={}
        )

    @property
    def user_related(self):
        u""" 関連ユーザー
        :param seed_user_id: ユーザーID
        """
        return bind_api(
            api=self,
            path='/user/related',
            payload_type='app_user',
            payload_list=True,
            allowed_param=['seed_user_id', 'filter'],
            require_param=['seed_user_id'],
            default_param={
                'filter': 'for_ios',
            }
        )

    @property
    def search_illust(self):
        u""" イラスト検索
        :param word: 検索キーワード
        :param duration: 検索期間 [within_last_day, within_last_week, within_last_month]
        :param search_target: 検索対象 [partial_match_for_tags(タグ部分一致), exact_match_for_tags(タグ完全一致), title_and_caption(タイトルキャプション)
        :param sort: ソート [date_desc, date_asc]
        :param offset: 検索開始位置のオフセット
        """
        return bind_api(
            api=self,
            path='/search/illust',
            payload_type='app_illust',
            payload_list=True,
            allowed_param=['word', 'duration', 'filter', 'search_target', 'sort', 'offset', 'page'],
            require_param=['word'],
            default_param={
                'filter': 'for_ios',
                'search_target': 'partial_match_for_tags',
                'sort': 'date_desc',
            }
        )

    @property
    def search_novel(self):
        u""" 小説検索
        :param word: 検索キーワード
        :param duration: 検索期間 [within_last_day, within_last_week, within_last_month]
        :param search_target: 検索対象 [partial_match_for_tags(タグ部分一致), exact_match_for_tags(タグ完全一致), title_and_caption(タイトルキャプション)
        :param sort: ソート [date_desc, date_asc]
        :param offset: 検索開始位置のオフセット
        """
        return bind_api(
            api=self,
            path='/search/novel',
            payload_type='app_novel',
            payload_list=True,
            allowed_param=['word', 'duration', 'search_target', 'sort', 'offset', 'page'],
            require_param=['word'],
            default_param={
                'search_target': 'partial_match_for_tags',
                'sort': 'date_desc',
            }
        )

    @property
    def search_user(self):
        u""" ユーザー検索
        :param word: 検索キーワード
        :param offset: 検索開始位置のオフセット
        """
        return bind_api(
            api=self,
            path='/search/user',
            payload_type='app_user',
            payload_list=True,
            allowed_param=['word', 'filter', 'offset', 'page'],
            require_param=['word'],
            default_param={
                'filter': 'for_ios',
            }
        )

    @property
    def search_autocomplete(self):
        return bind_api(
            api=self,
            path='/search/autocomplete',
            payload_type='app_auto_complete',
            payload_list=False,
            allowed_param=['word'],
            require_param=['word'],
            default_param={}
        )

    @property
    def ugoira_metadata(self):
        u""" うごイラメタデータ取得
        :param illust_id: イラストID
        """
        return bind_api(
            api=self,
            path='/ugoira/metadata',
            payload_type='app_metadata',
            payload_list=False,
            allowed_param=['illust_id'],
            require_param=['illust_id'],
            default_param={}
        )

    @property
    def illust_related(self):
        u""" 関連イラスト
        :param illust_id: イラストID
        """
        return bind_api(
            api=self,
            api_root='/v2',
            path='/illust/related',
            payload_type='app_illust',
            payload_list=True,
            allowed_param=['illust_id', 'filter'],
            require_param=['illust_id'],
            default_param={
                'filter': 'for_ios',
            }
        )

    @property
    def illust_comments(self):
        u""" イラストコメント
        :param illust_id: イラストID
        """
        return bind_api(
            api=self,
            path='/illust/comments',
            payload_type='app_comment',
            payload_list=True,
            allowed_param=['illust_id'],
            require_param=['illust_id'],
            default_param={}
        )

    @property
    def illust_bookmark_add(self):
        u""" イラストお気に入り追加
        :param illust_id: イラストID
        :param restrict: 公開／非公開 [public, private]
        :param tags: イラストタグ
        """
        return bind_api(
            api=self,
            api_root='/v2',
            method='POST',
            path='/illust/bookmark/add',
            payload_list=False,
            require_auth=True,
            allowed_param=['illust_id', 'restrict', 'tags'],
            require_param=['illust_id', 'restrict'],
            default_param={
                'restrict': 'public'
            }
        )

    @property
    def illust_bookmark_delete(self):
        u""" イラストお気に入り削除
        :param illust_id: イラストID
        """
        return bind_api(
            api=self,
            method='POST',
            path='/illust/bookmark/delete',
            payload_list=False,
            require_auth=True,
            allowed_param=['illust_id'],
            require_param=['illust_id'],
            default_param={}
        )

    @property
    def user_recommended(self):
        u""" ユーザーレコメンド
        """
        return bind_api(
            api=self,
            path='/user/recommended',
            payload_type='app_user',
            payload_list=True,
            allowed_param=['filter'],
            require_param=[],
            default_param={
                'filter': 'for_ios',
            }
        )

    @property
    def illust_recommended(self):
        u""" イラストレコメンド
        :param include_ranking_illusts: ランキングイラストを含める [True, False]
        """
        return bind_api(
            api=self,
            path='/illust/recommended',
            payload_type='app_illust',
            payload_list=True,
            require_auth=True,
            allowed_param=['include_ranking_illusts', 'filter'],
            require_param=[],
            default_param={
                'include_ranking_illusts': 'true',
                'filter': 'for_ios',
            }
        )

    @property
    def manga_recommended(self):
        u""" マンガレコメンド
        :param include_ranking_illusts: ランキングイラストを含める [True, False]
        """
        return bind_api(
            api=self,
            path='/manga/recommended',
            payload_type='app_illust',
            payload_list=True,
            require_auth=True,
            allowed_param=['include_ranking_illusts', 'filter'],
            require_param=[],
            default_param={
                'include_ranking_illusts': 'true',
                'filter': 'for_ios',
            }
        )

    @property
    def novel_recommended(self):
        u""" ノベルレコメンド
        :param include_ranking_illusts: ランキングイラストを含める [True, False]
        """
        return bind_api(
            api=self,
            path='/novel/recommended',
            payload_type='app_novel',
            payload_list=True,
            require_auth=True,
            allowed_param=['include_ranking_novels'],
            require_param=[],
            default_param={
                'include_ranking_novels': 'true',
            }
        )
