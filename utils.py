#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re

def abs_img_url(img_id, user_name, ext, prefix, page, thumb, posted_at, tags):
    img_list = []

    # 漫画
    if page:
        for p in range(0, page):
            img_list.append('http://i' + str(random.randint(1,2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(img_id) + '_big_p' + str(p) + '.' + ext)
    # うごイラ
    elif thumb and 'img-master' in thumb and 'うごイラ' in tags:
        img_list.append('http://i' + str(random.randint(1,2)) + '.pixiv.net/img-zip-ugoira/img/' + re.sub(r'( |-|:)', '/', str(posted_at)) + '/' + str(img_id) + '_ugoira600x600.zip')
    # イラスト
    else:
        img_list.append('http://i' + str(random.randint(1,2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(img_id) + '.' + ext)
    return img_list
