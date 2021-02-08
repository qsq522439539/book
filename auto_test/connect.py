# -*- coding:utf-8 -*-
# !/usr/bin/python3

import redis
import pymysql


test5_db_info = {"host": "zkt-hb02-test5.mysql.rds.aliyuncs.com",
                 "user": "zkt_test", "password": "zkt_test2016"}



def execute_db(sql, dict=0, database="zkt"):
    conn = pymysql.connect(**test5_db_info, database=database, port=3306)
    cursor = pymysql.cursors.DictCursor if dict else pymysql.cursors.Cursor
    cursor = conn.cursor(cursor=cursor)
    cursor.execute(sql, )
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

class ConnRedis(object):

    def  __init__(self, key, db=153):
        self.host = 'zkt-hb02-dev-out.redis.rds.aliyuncs.com'
        self.port = 6379
        self.password = 'zkt0613Zkt'
        self.key = key
        self.db =db
        self.conn = redis.Redis(host=self.host, port=self.port,password=self.password, db=self.db)

    def get(self):
        return self.conn.get(self.key)
        # return self.conn.keys()

    def set(self, value):
        self.conn.set(self.key, value)

    def delete(self):
        self.conn.delete(self.key)

    def get_ttl(self):
        return self.conn.ttl(self.key)


if __name__ == '__main__':
    data = execute_db("SELECT  * FROM ticket_product where ticket_product_id in (250956,250949)", 1)
    print(data)
    for key, value in data[0].items():
        if data[0][key] != data[1][key]:
            print('key:{}，自动创建值：{}，eb创建值：{}'.format(key, data[1][key], data[0][key]))