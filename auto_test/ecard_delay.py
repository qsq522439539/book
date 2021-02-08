# -*- coding:utf-8 -*-
# !/usr/bin/python3

import requests
from connect import execute_db

class TestEcard(object):

    def __init__(self, carno, hotel_id=184569):
        self.carno = ','.join([str(i) for i in carno])
        self.hotel_id = hotel_id

    def test_ecard(self):
        sql = "select a.ecard_product_carno as '卡号'," \
              "a.ecard_product_name as '产品名称', " \
              "a.available_date_to as '有效期'," \
              "a.status as '状态'," \
              "case when b.activate_date_type=0 then '时间区间' else '固定时间'  end as '激活时间类型'," \
              "activate_date_from as '激活开始时间'," \
              "activate_date_to  as '激活结束时间', " \
              "is_set_activate_time as '是否设置激活时间' " \
              "from ecard_ticket a inner join equity_card_date_snapshot b on a.ecard_ticket_id=b.ecard_ticket_id " \
              "where b.is_deleted=0 and  a.ecard_product_carno in ({}) and a.hotel_id={} and a.status!='refund' ".format(self.carno, self.hotel_id)
        print(sql)
        res = execute_db(sql, 1)
        print(res)
        for i in res:
            for key, value in i.items():
                print('{}: {}'.format(key, value))

    def test_apply(self):
        headers = {"accesstoken":"3b24dfc2-4fb5-4ca6-9076-2b2e158bcef7", "Content-Type":"application/json", "accept":"*/*"}
        apply_url = "http://test5-bg-api-gateway.zhiketong.net/ticket-api/eb/equity_delay/apply_delay?hotelId=184569"
        data = {"cardNoStr":self.carno,"dateType":0,"operateType":0,"delayReason":" ","hotelId":184569,"availableDays":1,"availableDateTo":"2021-01-07"}
        res = requests.post(apply_url, json=data, headers=headers).json()
        print(res)
        preViewKey = res['data']['preViewKey']
        return preViewKey


    def test_operate(self, preViewKey):
        headers = {"accesstoken":"3b24dfc2-4fb5-4ca6-9076-2b2e158bcef7", "Content-Type":"application/json", "accept":"*/*"}
        operate_url = "http://test5-bg-api-gateway.zhiketong.net/ticket-api/eb/equity_delay/operate_delay?hotelId=184569"
        operate_data = {"preViewKey": preViewKey, "hotelId": 184569}
        print(operate_data)
        res = requests.post(operate_url, headers=headers, json=operate_data)
        print(res.json())

if __name__ == '__main__':
    carno_list = [7001288,7001277]
    test = TestEcard(carno_list)
    # test.test_ecard()
    # preViewKey = test.test_apply()
    test.test_operate("a332f7bf-4b04-4222-95eb-10a3440b941f")