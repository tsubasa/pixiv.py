# -*- coding: utf-8 -*-

import random
import re

class PixivUtils(object):

    @staticmethod
    def abs_img_url(illust_id, user_name, ext, prefix, page, thumb, posted_at, tags):
        img_list = []

        if thumb and 'img-master' in thumb:
            if 'うごイラ' in tags:
                img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-zip-ugoira/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(illust_id) + '_ugoira600x600.zip')
            else:
                # http://i1.pixiv.net/img-original/img/2014/10/01/21/51/02/{illust_id}_p0.jpg
                # http://i1.pixiv.net/img-original/img/2014/10/01/21/51/02/{illust_id}_p1.jpg ...
                for p in range(0, int(page if page else 1)):
                    img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-original/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(illust_id) + '_p' + str(p) + '.' + ext)

        elif thumb and 'img-inf' in thumb:
            if page:
                for p in range(0, int(page)):
                    img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(illust_id) + '_big_p' + str(p) + '.' + ext)
            else:
                # http://i1.pixiv.net/img{prefix}/img/{user_name}/{illust_id}.jpg
                img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(illust_id) + '.' + ext)

        return img_list
