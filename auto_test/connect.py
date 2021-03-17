# -*- coding:utf-8 -*-
# !/usr/bin/python3

import redis
import pymysql
from warnings import filterwarnings


test5_db_info = {"host": "zkt-hb02-test5.mysql.rds.aliyuncs.com",
                 "user": "zkt_test", "password": "zkt_test2016"}
release_db_info = {"host": "zkt-hd01-f-pro-mdb-s-rds-01.zhiketong.cn",
                 "user": "wangyu", "password": "nNfxHbx4Ha"}

def execute_db(sql, dict=0, database="zkt", test_env=1):
    filterwarnings("ignore",category=pymysql.Warning)
    db = test5_db_info if test_env else release_db_info
    conn = pymysql.connect(**db, database=database, port=3306)
    cursor = pymysql.cursors.DictCursor if dict else pymysql.cursors.Cursor
    cursor = conn.cursor(cursor=cursor)
    cursor.execute(sql, )
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


class ConnRedis(object):

    def  __init__(self, db=153):
        self.host = 'zkt-hb02-dev-out.redis.rds.aliyuncs.com'
        self.port = 6379
        self.password = 'zkt0613Zkt'
        self.db = db
        self.conn = redis.Redis(host=self.host, port=self.port, password=self.password, db=self.db)

    def get(self, key):
        return self.conn.get(key)
        # return self.conn.keys()

    def set(self, key, value):
        self.conn.set(key, value)

    def delete(self, key):
        self.conn.delete(key)

    def get_ttl(self, key):
        return self.conn.ttl(key)


if __name__ == '__main__':
    data = execute_db("SELECT  * FROM ticket_product where ticket_product_id in (250956,250949)", 1)
    print(data)
    for key, value in data[0].items():
        if data[0][key] != data[1][key]:
            print('key:{}，自动创建值：{}，eb创建值：{}'.format(key, data[1][key], data[0][key]))
