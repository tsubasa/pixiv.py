#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from api import PixivApi, PixivSearch, PixivResultParser
from config import config, args
from manager import MySQLdbManager

logging.basicConfig(filename=config.common.log_file, format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
conn = MySQLdbManager(host=config.mysql.host, user=config.mysql.user, passwd=config.mysql.passwd, db=config.mysql.db)

def pixiv_bot():
    api = PixivApi(config.pixiv.user, config.pixiv.passwd)
    search = PixivSearch(api)
    search.set_order()
    search.set_keyword(args.keyword)

    while True:
        raw_data = search.search()
        if not raw_data or search.page > args.page:
            break;

        ret = PixivResultParser(raw_data)
        rows = ret.get_row_all()
        for row in rows:
            conn.insert_illust(row)

        # time.sleep(1)
        search.next()

    logging.info('end')

if __name__ == '__main__':
    logging.info('start')
    logging.info('keyword: %s' % args.keyword)
    try:
        pixiv_bot()
    except Exception as e:
        logging.exception(e)
