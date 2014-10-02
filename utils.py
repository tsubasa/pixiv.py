#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re

def abs_img_url(img_id, user_name, ext, prefix, page, thumb, posted_at, tags):
    img_list = []

    # TODO : img-inf または imf-master で処理を分岐

    # 漫画
    if thumb and 'img-inf' in thumb and page:
        for p in range(0, page):
            img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(img_id) + '_big_p' + str(p) + '.' + ext)
    elif thumb and 'img-master' in thumb and page:
        # http://i1.pixiv.net/img-original/img/2014/10/01/21/51/02/{illust_id}_p0.jpg
        # http://i1.pixiv.net/img-original/img/2014/10/01/21/51/02/{illust_id}_p1.jpg ...
        for p in range(0, page):
            img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-original/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(img_id) + '_p' + str(p) + '.' + ext)

    # うごイラ
    elif thumb and 'img-master' in thumb and u'うごイラ' in tags:
        img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-zip-ugoira/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(img_id) + '_ugoira600x600.zip')

    # イラスト
    elif thumb and 'img-inf' in thumb:
        # http://i1.pixiv.net/img{prefix}/img/{user_name}/{illust_id}.jpg
        img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(img_id) + '.' + ext)
    elif thumb and 'img-master' in thumb:
        # http://i2.pixiv.net/img-original/img/2014/10/02/07/46/59/{illust_id}_p0.jpg
        img_list.append('http://i' + str(random.randint(1, 2)) + '.pixiv.net/img-original/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(img_id) + '_p0' + '.' + ext)

    return img_list
