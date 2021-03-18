# -*- coding:utf-8 -*-
# !/usr/bin/python3

import json
import decimal
from connect import execute_db

class CommonAssert(object):

    def __init__(self, platform_order_id):
        self.platform_order_id = platform_order_id
        self.env = 1

    def get_res(self, sql):
        res = execute_db(sql, 1, test_env=self.env)
        for n,value in enumerate(res):
            for k, v in value.items():
                print("{}: {}".format(k, v))
            print("="*50)
        return res

    def get_ticket_order(self):
        # deduction 优惠
        sql = "select ticket_product_id,member_id,quantity,price,paid,deduction,refund,from_type,from_id,settle_condition," \
              "item_channel_commission,item_share_commission,item_agent_commission,item_customer_commission,item_weekend_commission," \
              "pay_channel,order_no,order_detail_id " \
              "from ticket_order " \
              "where platform_order_id={}".format(self.platform_order_id)
        print("ticket_order表数据".center(100, '*'))
        self.get_res(sql)

    def get_ticket_coupon(self):
        # ticket_order_deduction_amount:'预售订单抵扣金额, 单位分'
        # coupon_amount:'红包金额, 单位分'
        # promotion_type:'促销类型1-红包;2-砍价;3-拼团,4-满减,5-定金膨胀,6-会员价'
        # product_spec_type:'多规格产品标识，0.非多规格，1.大P产品，2.小p产品'
        # promotion_desc:'优惠描述信息'
        sql = "select ticket_coupon_order_id,ticket_order_id,ticket_order_price,ticket_order_deduction_amount,coupon_amount,promotion_type,product_spec_type,promotion_desc" \
              " from zkt.ticket_coupon_order " \
              "where  ticket_order_id in (select ticket_order_id from zkt.ticket_order where platform_order_id={})".format(self.platform_order_id)
        print("ticket_coupon表数据".center(100, '*'))
        self.get_res(sql)

    def get_order_no(self):
        sql = "select sale_order_no,relevance_order_no from zkt_order_center.sale_order where platform_order_id={}".format(self.platform_order_id)
        res = execute_db(sql, 1, test_env=self.env)
        res = res[0] if res else False
        return res

    def get_ticket_post(self):
        sql = "select a.amount,b.* from zkt.ticket_order_charge_details a  inner join zkt.ticket_order_post b " \
              "on a.ticket_order_id=b.ticket_order_id " \
              "where a.ticket_order_id in (select ticket_order_id from ticket_order where platform_order_id={})".format(self.platform_order_id)
        print("get_ticket_post、ticket_order_charge_details表数据".center(100, '*'))
        self.get_res(sql)

    def get_sale_order(self):
        # status:'状态(0:初始创建,1:待付款,2:部分支付完成,3:支付完成4:交易完成,5:退款中,6:已退款,7:交易取消)'
        # order_way:'下单方式（0:普通下单 1:购物车下单 2:多规格下单）'
        # assign_member_level_source:指定会员等级来源(1:代客下单,2:权益卡引导,3:储值卡充值引导,4:正常购买,为了支持会员多体系,5:日历房特殊的等级)'
        # relevance_order_no:'关联订单ID（目前用于微POS订单与储值卡引导之间的关联）
        # prepay_consume_model:'订单储值消费模式（0：正常订单,1:充值消费订单）'
        # post_ship_type:'邮寄方式（none:无,mail:邮寄,self_take:自提）'
        if not self.get_order_no():
            return
        relevance_order_no = self.get_order_no()['relevance_order_no']
        if relevance_order_no:
            sql = "select a.sale_order_no,a.member_id,a.member_level,a.member_level_name,a.status,a.platform_order_id," \
                  "a.total_price,a.total_pay_price,a.order_way,a.assign_member_level_id,a.assign_member_level_source,a.relevance_order_no,a.prepay_consume_model,a.post_ship_type," \
                  "b.product_id,b.product_type,b.total_price,b.total_paid_price,b.buy_quantity,b.refund_quantity,b.refund_price,b.no_discount_amount " \
                  "from zkt_order_center.sale_order a inner join zkt_order_center.sale_order_detail b on a.sale_order_no = b.sale_order_no " \
                  "where a.relevance_order_no={} or a.sale_order_no={}".format(relevance_order_no, relevance_order_no)
        else:
            sql = "select a.sale_order_no,a.member_id,a.member_level,a.member_level_name,a.status,a.platform_order_id," \
                  "a.total_price,a.total_pay_price,a.order_way,a.assign_member_level_id,a.assign_member_level_source,a.relevance_order_no,a.prepay_consume_model,a.post_ship_type," \
                  "b.product_id,b.product_type,b.total_price,b.total_paid_price,b.refund_quantity,b.refund_price,b.no_discount_amount " \
                  "from zkt_order_center.sale_order a inner join zkt_order_center.sale_order_detail b on a.sale_order_no = b.sale_order_no " \
                  "where a.platform_order_id={}".format(self.platform_order_id)
        print("sale_order、sale_order_detail表数据".center(100, '*'))
        self.get_res(sql)

    def get_sale_post(self):
        if not self.get_order_no():
            return
        sale_order_no = self.get_order_no()['sale_order_no']
        sql = "select province_id,city_id,area_id,post_price,post_address from zkt_order_center.sale_order_post where sale_order_no={}".format(sale_order_no)
        print("sale_order_post表数据".center(100, '*'))
        self.get_res(sql)

    def get_ticket_settlement_log(self):
        sql = "select * from zkt.ticket_settlement_log where ticket_id in (select ticket_id from zkt.ticket where platform_order_id={})".format(self.platform_order_id)
        print("settlement_log表数据".center(100, '*'))
        self.get_res(sql)

    def get_post_settlement_log(self):
        sql = "select * from zkt.postage_settlement_log where order_id in (select ticket_order_id from zkt.ticket_order where platform_order_id={})".format(self.platform_order_id)
        print("post_settlement_log表数据".center(100, '*'))
        self.get_res(sql)

    def get_post(self):
        sql = "SELECT c.mailing_information_id,b.ticket_order_id,a.associate_id,a.product_name,b.ticket_name,a.third_code,a.insured_amount," \
              "c.comment,c.post_number,b.status,b.ticket_order_id,c.sender_mobile,c.sender_name,c.send_address,c.service_provider," \
              "c.post_status,c.comment,c.receiver_name,c.receive_address,c.receive_mobile,c.hotel_id " \
              "FROM zkt_post.mailing_information_item a " \
              "LEFT JOIN zkt.ticket b ON a.associate_id = b.ticket_id " \
              "LEFT JOIN zkt_post.mailing_information c ON a.mailing_information_id = c.mailing_information_id " \
              "WHERE b.platform_order_id ={}".format(self.platform_order_id)
        print("mailing_information表数据".center(100, '*'))
        self.get_res(sql)

    def main(self):
        self.get_sale_order()
        self.get_ticket_order()
        self.get_ticket_coupon()
        self.get_ticket_settlement_log()
        self.get_post_settlement_log()
        self.get_post()
        self.get_ticket_post()
        self.get_sale_post()

if __name__ == '__main__':
    CommonAssert('1322860969').main()
