from Database import database
from Enum.Enums import enum_login_type


spliter = ':!!:'


def signup_level_1(data):
    name = data[0]
    username = data[1]
    password = data[2]

    query = """
            select id from tbl_user where username='%s'
    """ % username
    db = database()
    result = db.select(query)

    if result is not None:
        db.close()
        return 'duplicate username'

    #### add user

    from Tools import get_date
    now = get_date()

    query = """
            insert into tbl_user (username, password, name, date, active)
            values
            ('%s', '%s', '%s', '%s', %d)
    """ % (username, password, name, now, 1)
    result = db.insert(query)

    if not result:
        return 'false'

    query = """
            select id from tbl_user where username='%s'
    """ % username
    result = db.select(query)

    if result is None:
        return 'false'

    result = result[0][0]
    db.close()
    return result


def signup_level_2(data):
    id = int(data[0])
    avatar = int(data[1]) if len(data[1]) > 0 else None
    city = int(data[2]) if len(data[2]) > 0 else None
    phonenumber = data[3] if len(data[3]) > 0 else None
    favorite_game = int(data[4]) if len(data[4]) > 0 else None
    credit_card = data[5] if len(data[5]) > 0 else None
    email = data[6] if len(data[6]) > 0 else None

    query = """
            update tbl_user set
            avatar=%d
            , city=%d
            , phonenumber='%s'
            , favorite_game=%d
            , credit_card_number='%s'
            , email='%s'
            where id=%d
    """ % (avatar, city, phonenumber, favorite_game, credit_card, email, id)
    db = database()
    result = db.update(query)

    if not result:
        return 'false'

    db.close()

    result = 'true'
    return result


def get_next_game(id):
    id = int(id)
    query_get_date = """
        SELECT tbl_league_playing.date FROM tbl_league_playing
        join tbl_league_playing_user
        on tbl_league_playing_user.id_league_playing=tbl_league_playing.id
        where tbl_league_playing_user.id_user=%d
        order by tbl_league_playing.date desc
        limit 1
    """ % id

    query_get_competitor_name = """
        select name from tbl_league_playing_user
        join tbl_user
        on tbl_user.id=tbl_league_playing_user.id_user
        where id_league_playing=(select id_league_playing from tbl_league_playing_user where id_user=%d)
        and id_user!=%d
    """ % (id, id)

    query_get_league_name = """
        select name from tbl_competition
        join tbl_league
        join tbl_league_player
        on tbl_league_player.id_league=tbl_league.id
        and tbl_league.id_competition=tbl_competition.id
        where tbl_league_player.id_user=%d
    """ % id

    db = database()
    league_name = db.select(query_get_league_name)
    if league_name is not None:
        league_name = league_name[0][0]
    else:
        league_name = ''

    competitor_name = db.select(query_get_competitor_name)
    if competitor_name is not None:
        competitor_name = competitor_name[0][0]
    else:
        competitor_name = ''

    league_date = db.select(query_get_date)
    if league_date is not None:
        league_date = str(league_date[0][0])
    else:
        league_date = ''

    db.close()
    import json
    result = [competitor_name , league_date , league_name]
    result = json.dumps(result)
    return result
