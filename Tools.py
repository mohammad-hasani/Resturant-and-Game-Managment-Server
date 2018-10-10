from Database import database
from datetime import datetime


def get_user_price_by_card_id(username):
    query = "select price from tbl_user where username='%s' limit 1" % (username)
    db = database()
    price = db.select(query)[0][0]
    db.close()
    return price


def update_user_price_by_card_id(username, price):
    # query = "select price from tbl_user where card_id=%'s' limit 1"
    # db = database()
    # result = db.select(query)
    # db.close()
    #
    # current_price = result[0][0]
    # if int(current_price) < price:
    #     return 'no credit'


    query = """update tbl_user, (SELECT * FROM tbl_user where username='%s' limit 1) src
    set tbl_user.price=src.price - %d
    where tbl_user.id=src.id""" % (username, int(price))
    db = database()
    result = db.update(query)
    db.close()
    return result


def get_date():
    now = datetime.now()
    return now


def get_sliders():
    query = """select id, name, url from tbl_slider limit 5"""
    db = database()
    result = db.select(query)
    db.close()
    if result is None:
        return 'false'
    import ConvertData
    result = ConvertData.ConvertData().convert_to_json(result)
    return result


def get_usere_id_by_username(username):
    query = "select id from tbl_user where username=''" % username
    db = database()
    result = db.select(query)
    result = result[0][0]
    db.close()
    return result
