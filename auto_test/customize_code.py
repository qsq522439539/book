# -*- coding:utf-8 -*-
# !/usr/bin/python3

from connect import *

CUSTOMIZE_CARD_REDIS_KEY_PREFIX = 'ticket-api:customize_card'


class CustomizeCode(object):

    def __init__(self, hotel_id, product_id):
        self.hotel_id = hotel_id
        self.product_id = product_id
        self.key = self.gen_key()
        self.redis = ConnRedis(self.key)

    def gen_key(self):
        return '_'.join([CUSTOMIZE_CARD_REDIS_KEY_PREFIX, str(self.hotel_id), str(self.product_id)])

    def get_code(self):
        print(self.key)
        code = self.redis.get()
        print(code)

    def set_code(self, code):
        self.redis.set(code)

    def get_ttl(self):
        ttl = self.redis.get_ttl()
        print(ttl)
        return ttl

    def delete(self):
        self.redis.delete()


if __name__ == '__main__':
    customize_code = CustomizeCode(184569, 242466)
    customize_code.set_code(27)
    customize_code.get_code()
    # customize_code.delete()
