from ConvertData import ConvertData
import datetime
from Database import database
import Tools


def order_food(data):
    username = data[0]
    admin_id = int(data[1])
    info = data[2]
    info = ConvertData().convert_from_json(info)
    now_date = datetime.datetime.now()

    # credit = Tools.get_user_price_by_card_id(username)

    price = 0

    for index, value in enumerate(info):
        db = database()
        query = "select price from tbl_facility where id=%d limit 1" % (value[0])
        result = db.select(query)
        current_price = result[0][0]

        current_price -= current_price

        current_price *= int(value[1])
        price += current_price
        db.close()

    # if credit < price:
    #     return 'no credit'

    result = Tools.update_user_price_by_card_id(username, price)

    if result is False:
        return False

    for index, value in enumerate(info):
        query = """insert into tbl_order (id_user, id_facility, count, active, is_delivered, date, id_admin)
                   values
                   ((select id from tbl_user where username='%s' limit 1), %d, %d, 0, 0, '%s', %d)""" % \
                (username, int(value[0]), int(value[1]), now_date, admin_id)
        db = database()
        result = db.insert(query)
        if result is False:
            return False
        db.close()
    return True


def get_foot_orders(data):
    admin_id = int(data[0])
    query = """select tbl_order.id, tbl_user.name, tbl_facility.name, tbl_order.count from tbl_order
                join tbl_user
                join tbl_facility
                on tbl_order.id_user=tbl_user.id and tbl_order.id_facility=tbl_facility.id
                where tbl_order.is_delivered=0
                and tbl_order.id_admin=%d
                limit 200""" % admin_id
    db = database()
    result = db.select(query)
    db.close()
    result = ConvertData().convert_to_json(result)
    return result
