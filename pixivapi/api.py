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
            raise TypeError('パーサーオブジェクトのインスタンスが異なります')

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
            required_param=['id'],
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
            required_param=['id'],
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
            required_param=['q'],
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
            raise TypeError('パーサーオブジェクトのインスタンスが異なります')

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
            required_param=['user_id'],
            default_param={}
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
            required_param=['user_id'],
            default_param={
                'filter': 'for_ios',
            }
        )

    @property
    def search_illust(self):
        u""" 作品検索
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
            required_param=['word'],
            default_param={
                'filter': 'for_ios',
                'search_target': 'partial_match_for_tags',
                'sort': 'date_desc',
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
            required_param=['word'],
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
            required_param=['illust_id'],
            default_param={}
        )

    @property
    def illust_related(self):
        u""" 関連イラスト
        :param illust_id: イラストID
        """
        return bind_api(
            api=self,
            path='/illust/related',
            payload_type='app_illust',
            payload_list=True,
            allowed_param=['illust_id', 'filter'],
            required_param=['illust_id'],
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
            required_param=['illust_id'],
            default_param={}
        )
