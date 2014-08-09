#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def abs_img_url(img_id, user_name, ext, prefix, page):
    img_list = []
    if page:
        for p in range(0, page):
            img_list.append('http://i' + str(random.randint(1,2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(img_id) + '_big_p' + str(p) + '.' + ext)
    else:
        img_list.append('http://i' + str(random.randint(1,2)) + '.pixiv.net/img' + str(prefix).zfill(2) + '/img/' + user_name + '/' + str(img_id) + '.' + ext)
    return img_list
