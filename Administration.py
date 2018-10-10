from Database import database
from Enum.Enums import enum_login_type
from Tools import get_date


def login(data):
    if data[0] == 'admin':
        type = enum_login_type.Admin
    elif data[0] == 'player':
        type = enum_login_type.Player
    username = data[1]
    password = data[2]

    if type == enum_login_type.Admin:
        query = """
            select id from tbl_admin where username='%s' and password='%s'
        """ % (username, password)
    elif type == enum_login_type.Player:
        query = """
            select id from tbl_user where username='%s' and password='%s'
        """ % (username, password)
    db = database()
    result = db.select(query)
    if result is not None:
        result = result[0][0]
    else:
        result = 'false'
    db.close()
    return result


def get_admins_list(info):
    city_id = info[0]
    query = """
        select id, name from tbl_admin"""
    # where city_id=%d
    # """ % city_id

    db = database()
    result = db.select(query)
    db.close()
    if result is None:
        return 'false'
    import ConvertData
    result = ConvertData.ConvertData().convert_to_json(result)
    return result


def get_admin_description(id):
    id = int(id[0])
    query = "select description from tbl_admin where id=%d" % id
    db = database()
    result = db.select(query)[0][0]
    db.close()
    if result is None:
        return 'false'
    return result













