# -*- coding:utf-8 -*-
# !/usr/bin/python3

from connect import execute_db

if __name__ == '__main__':
    sql1 = "select ap.product_id,ap.product_name from activity_product ap inner join activity a on ap.activity_id = a.id where a.is_delete = 0 and a.activity_type = 18 and ap.product_name is not  null"
    result = execute_db(sql1,database='zkt_promotion')
    data = {i[0]: i[1] for i in result}
    for key, value in data.items():
        sql = 'select product_name from ticket_product where ticket_product_id={}'.format(key)
        try:
            name = execute_db(sql)[0][0]
        except IndexError as e:
            name = ''
        assert name == value
