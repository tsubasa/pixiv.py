# -*- coding: utf-8 -*-

from utils import PixivUtils

class PixivModel(object):

    """
    :param row[0]   : illust_id
    :param row[1]   : user_id
    :param row[2]   : extension
    :param row[3]   : image title
    :param row[4]   : image directory prefix
    :param row[5]   : display_name
    :param row[6]   : mobile thumbnail (128x128) /img-inf/ or /img-master/
    :param row[7]   : unused/empty
    :param row[8]   : unused/empty
    :param row[9]   : mobile thumbnail (480mw)
    :param row[10]  : unused/empty
    :param row[11]  : unused/empty
    :param row[12]  : upload date
    :param row[13]  : space-delimited list of tags
    :param row[14]  : drawing software (e.g. SAI)
    :param row[15]  : number of ratings
    :param row[16]  : total score (sum of all ratings)
    :param row[17]  : number of views
    :param row[18]  : image description (raw HTML)
    :param row[19]  : number of pages (empty if not a manga sequence)
    :param row[20]  : unused/empty
    :param row[21]  : unused/empty
    :param row[22]  : number of favorites
    :param row[23]  : number of comments
    :param row[24]  : artist username
    :param row[25]  : unused/empty
    :param row[26]  : R-18 marker (0 is safe, 1 is R-18, 2 is R-18G)
    :param row[27]  : novel series id (blank for illustrations and novels not part of a series)
    :param row[28]  : unused/empty
    :param row[29]  : mobile profile image
    :param row[30]  : unused/empty
    """
    # @see https://danbooru.donmai.us/wiki_pages/58938 #Explanation of result fields for works

    @classmethod
    def parse(cls, row):
        raise NotImplementedError

    @classmethod
    def parse_list(cls, rows):
        results = []
        for row in rows:
            if row:
                results.append(cls.parse(row))
        return results

class PixivIllustModel(PixivModel):

    @classmethod
    def parse(cls, row):
        setattr(cls, 'id', row[0])
        setattr(cls, 'user_id', row[1])
        setattr(cls, 'extension', row[2])
        setattr(cls, 'title', row[3])
        setattr(cls, 'prefix', row[4])
        setattr(cls, 'display_name', row[5])
        setattr(cls, 'thumb', row[6])
        setattr(cls, 'posted_at', row[12])
        setattr(cls, 'tags', row[13].split())
        setattr(cls, 'tool', row[14])
        setattr(cls, 'rated_count', row[15])
        setattr(cls, 'score_count', row[16])
        setattr(cls, 'view_count', row[17])
        setattr(cls, 'description', row[18])
        setattr(cls, 'page', row[19])
        setattr(cls, 'favorites_count', row[22])
        setattr(cls, 'comments_count', row[23])
        setattr(cls, 'user_name', row[24])
        setattr(cls, 'r18', row[26])
        setattr(cls, 'imgs', PixivUtils.abs_img_url(row[0], row[24], row[2], row[4], row[19], row[6], row[12], row[13]))
        return cls

class PixivNovelModel(PixivModel):

    @classmethod
    def parse(cls, row):
        setattr(cls, 'id', row[0])
        setattr(cls, 'user_id', row[1])
        setattr(cls, 'title', row[3])
        setattr(cls, 'display_name', row[5])
        setattr(cls, 'thumb', row[6])
        setattr(cls, 'posted_at', row[12])
        setattr(cls, 'tags', row[13].split())
        setattr(cls, 'rated_count', row[15])
        setattr(cls, 'score_count', row[16])
        setattr(cls, 'view_count', row[17])
        setattr(cls, 'description', row[18])
        setattr(cls, 'page', row[19])
        setattr(cls, 'favorites_count', row[22])
        setattr(cls, 'comments_count', row[23])
        setattr(cls, 'user_name', row[24])
        setattr(cls, 'r18', row[26])
        return cls

class PixivUserModel(PixivModel):

    @classmethod
    def parse(cls, row):
        setattr(cls, 'user_id', row[1])
        setattr(cls, 'display_name', row[5])
        setattr(cls, 'thumb', row[6])
        setattr(cls, 'user_name', row[24])
        return cls
