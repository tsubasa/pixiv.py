# -*- coding: utf-8 -*-

import MySQLdb

class MySQLdbManager:
    """MySQLdb manager"""

    last_query = ''

    def __init__(self, host, user, passwd, db, port=3306, charset='utf8mb4'):
        try:
            self.connect = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset)
            self.set_dict_cursor()
        except MySQLdb.Error as e:
            raise Exception(e)

    def __del__(self):
        if self.cursors:
            self.cursors.close()
        if self.connect:
            self.connect.close()

    def close_cursor(self):
        if self.cursors:
            self.cursors.close()

    def set_cursor(self):
        self.cursors = self.connect.cursor(MySQLdb.cursors.Cursor)

    def set_dict_cursor(self):
        self.cursors = self.connect.cursor(MySQLdb.cursors.DictCursor)

    def get_last_insert_id(self):
        return self.cursors.lastrowid

    def get_last_query(self):
        return self.last_query

    def _insert(self, sql, param=()):
        try:
            self._execute(sql, param)
            self.connect.commit()
        except MySQLdb.Error as e:
            self.connect.rollback()
            raise Exception(e)

    def _fetchall(self, sql, param=()):
        try:
            self._execute(sql, param)
            return self.cursors.fetchall()
        except MySQLdb.Error as e:
            raise Exception(e)

    def _fetchone(self, sql, param=()):
        try:
            self._execute(sql, param)
            return self.cursors.fetchone()
        except MySQLdb.Error as e:
            raise Exception(e)

    def _execute(self, sql, param=()):
        self.last_query = ' '.join((sql % param).split())
        self.cursors.execute(sql, param)

    """
    `id` int(12) unsigned NOT NULL,
    `user_id` int(12) unsigned NOT NULL,
    `user_id_name` varchar(20) NOT NULL,
    `title` varchar(255) NOT NULL,
    `description` text NULL,
    `post_name` varchar(50) NOT NULL,
    `posted_at` timestamp NULL DEFAULT NULL,
    `extension` varchar(10) NOT NULL,
    `prefix` int(4) NOT NULL,
    `tags` varchar(255) NULL,
    `tools` varchar(100) NULL,
    `page` int(4) NULL,
    `preview` int(10) NOT NULL DEFAULT 0,
    `score` int(10) NOT NULL DEFAULT 0,
    `reviewer` int(10) NOT NULL DEFAULT 0,
    `r18` tinyint(1) NOT NULL DEFAULT FALSE,
    `saved_at`  timestamp NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

    id              : data[0]
    user_id         : data[1]
    user_id_name    : data[24]
    title           : data[3]
    description     : data[18]
    post_name       : data[5]
    posted_at       : data[12]
    extension       : data[2]
    prefix          : data[4]
    tags            : data[13]
    tools           : data[14]
    page            : data[19]
    preview         : data[17]
    score           : data[16]
    reviewer        : data[15]
    r18             : data[26]
    """

    # イラストデータ登録
    def insert_illust(self, data):
        param = {}
        param['id'] = data[0]
        param['user_id'] = data[1]
        param['user_id_name'] = data[24]
        param['title'] = data[3]
        param['description'] = data[18]
        param['post_name'] = data[5]
        param['posted_at'] = data[12]
        param['extension'] = data[2]
        param['prefix'] = data[4]
        param['tags'] = data[13]
        param['tools'] = data[14]
        param['page'] = data[19] if data[19] else None
        param['preview'] = data[17]
        param['score'] = data[16]
        param['reviewer'] = data[15]
        param['r18'] = True if int(data[26]) else False

        col = ', '.join(list(map(lambda x: x, param)))
        value = ', '.join(list(map(lambda x: '%s', param)))

        sql = """INSERT INTO px_illust(%s) VALUES(%s)
                 ON DUPLICATE KEY
                 UPDATE tags = VALUES(tags), preview = VALUES(preview), score = VALUES(score), reviewer = VALUES(reviewer), description = VALUES(description)
                 """ % (col, value)

        self.cursors.execute(sql, param.values())
        self.connect.commit()

    def get_not_saved(self):
        self.cursors.execute("""SELECT id, user_id, user_id_name, extension, prefix, page FROM px_illust WHERE saved_at IS NULL AND deleted_at IS NULL LIMIT 1000""")
        return self.cursors.fetchall()

    # イラストダウンロードフラグ
    def update_illust_save(self, illust_id):
        self.cursors.execute('UPDATE px_illust SET saved_at = NOW() WHERE id = %s', (illust_id,))
        self.connect.commit()

    # イラスト削除フラグ
    def update_illust_delete(self, illust_id):
        self.cursors.execute('UPDATE px_illust SET deleted_at = NOW() WHERE id = %s', (illust_id,))
        self.connect.commit()
