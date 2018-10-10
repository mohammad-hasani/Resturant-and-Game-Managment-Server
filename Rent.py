from datetime import datetime
from Database import database
import Tools

def analysis(data):
    card_id = data[0]
    game_id = data[1]
    datetime_now = datetime.now()

    query = """
        select end_time from tbl_rent
        where
        id_user=(select id from tbl_user where card_id='%s' limit 1)
        and
        id_game=%d
        limit 1
    """ % (card_id, game_id)

    db = database()
    result = db.select(query)
    db.close()
    if result is None:
        query = """
            select if((
            select device_count from tbl_game
            where id=%d limit 1)
            >=
            (select count(id) from tbl_rent
             where id_game=%d and end_time is null)
             , 1, -1)
        """ % (game_id, game_id)

        db = database()
        result = db.select(query)
        db.close()

        if result == 1:
            result = start_rent(card_id, game_id, datetime_now)
            return result
        elif result == -1:
            return 'no device'

    else:
        end_rent(card_id, game_id, datetime_now)

        end_time = datetime_now

        total_seconds = end_time - datetime_now
        total_seconds = total_seconds.total_seconds()

        query = """select price_per_hour from tbl_game where id=%d""" % (game_id)

        db = database()
        result = db.select(query)
        db.close()

        price_per_hour = result[0][0]

        pay = price_per_hour / 3600
        pay *= total_seconds
        result = Tools.update_user_price_by_card_id(card_id, pay)

        return result


def start_rent(card_id, game_id, datatime_now):
    query = """
        insert into tbl_rent
        (id_user, id_game, start_time)
        values
        ((select id from tbl_user where card_id='%s'), %d, '%s')
    """ % (card_id, game_id, datatime_now)

    db = database()
    result = db.update(query)
    db.close()

    return result


def end_rent(card_id, game_id, datetime_now):

    query = """
        update tbl_rent set
        end_time='%s'
        where
        id_user=(select id from tbl_user where card_id='%s')
        and
        id_game='%s'
    """ % (datetime_now, card_id, game_id)

    db = database()
    result = db.update(query)
    db.close()

    return result