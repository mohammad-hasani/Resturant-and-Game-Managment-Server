import Enum
from Database import database
from ConvertData import ConvertData
from Enum.Enums import enum_competition_type
from Tools import get_date


def new_competition(data):
    nickname = data[0]
    id_game = int(data[1])
    competition_type = enum_competition_type(int(data[2]))
    team_count = int(data[3])
    signup_date = data[4]
    start_date = data[5]
    admin_id = int(data[6])

    query = """
        insert into tbl_competition
        (id_game, count, date_signup, date_start, name, admin_id)
        values
        (%d, %d, '%s', '%s', '%s', %d)
    """ % (id_game, team_count, signup_date, start_date, nickname, admin_id)

    db = database()
    result = db.insert(query)
    query = """
        select id from tbl_competition where name='%s'
        order by name DESC
    """ % (nickname)
    result = db.select(query)
    db.close()

    competition_id = (result[0][0])

    result = None

    if competition_type == enum_competition_type.Tournament:
        query = """
            insert into tbl_tournament
            (id_competition, status)
            values
            (%d, %d)
        """ % (competition_id, -2)

        db = database()
        result = db.insert(query)
        db.close()

    elif competition_type == enum_competition_type.League:
        query = """
            insert into tbl_league
            (id_competition)
            values
            (%d)
        """ % (competition_id)

        db = database()
        result = db.insert(query)
        db.close()

    return result


def get_games_list():
    query = "select id, name from tbl_game"
    db = database()
    result = db.select(query)
    db.close()
    result = ConvertData().convert_to_json(result)
    return result


def signup_to_competition_by_cardid(data, type):
    card_id = data[0]
    status = -1
    if type == enum_competition_type.League:
        league_id = int(data[1])
        query = """
            INSERT INTO tbl_league_player ( id_user, id_league, status )
            VALUES((SELECT id FROM tbl_user WHERE card_id='%s'), %d, %d)
        """ % (card_id, league_id, status)
    elif type == enum_competition_type.Tournament:
        tournament_id = int(data[1])
        query = """
            INSERT INTO tbl_tournament_player ( id_user, id_tournament, status )
            VALUES((SELECT id FROM tbl_user WHERE card_id='%s'), %d, %d)
        """ % (card_id, tournament_id, status)

    db = database()
    result = db.insert(query)
    db.close()
    return result


def signup_to_competition_by_userid(data, type):
    user_id = data[0]
    status = -1
    if type == enum_competition_type.League:
        league_id = int(data[1])
        query = """
            INSERT INTO tbl_league_player ( id_user, id_league, status )
            VALUES(%d, %d, %d)
        """ % (user_id, league_id, status)
    elif type == enum_competition_type.Tournament:
        tournament_id = int(data[1])
        query = """
            INSERT INTO tbl_tournament_player ( id_user, id_tournament, status )
            VALUES(%d, %d, %d)
        """ % (user_id, tournament_id, status)

    db = database()
    result = db.insert(query)
    db.close()
    return result


def get_competition_info(info):
    type = int(info[0])
    if type == 0:
        type = enum_competition_type.League
    elif type == 1:
        type = enum_competition_type.Tournament
    game_id = int(info[1])
    city_id = int(info[2])
    query = ""

    if type == enum_competition_type.League:
        query = """
            select tbl_competition.id, tbl_competition.count, tbl_competition.name from tbl_competition
            join tbl_league
            on tbl_league.id_competition=tbl_competition.id
            where tbl_competition.city=%d and tbl_competition.id_game=%d
        """ % (city_id, game_id)
    elif type == enum_competition_type.Tournament:
        query = """
            select tbl_competition.id, tbl_competition.count, tbl_competition.name from tbl_competition
            join tbl_tournament
            on tbl_tournament.id_competition=tbl_competition.id
            join tbl_admin
            on tbl_admin.id=tbl_competition.admin_id
            where tbl_admin.city_id=%d and tbl_competition.id_game=%d
        """ % (city_id, game_id)

    db = database()
    result = db.select(query)
    db.close()
    if result is None:
        return 'false'
    import ConvertData
    result = ConvertData.ConvertData().convert_to_json(result)
    return result


def get_next_competition(info):
    admin_id = int(info[0])
    now_date = get_date()

    query = """
        select tbl_competition.name, tbl_competition.date_start, tbl_game.name from tbl_competition
        join tbl_game
        on tbl_competition.id_game=tbl_game.id
        where tbl_competition.admin_id=%d
        and tbl_competition.date_start > '%s'
        order by tbl_competition.date_start
        limit 1
    """ % (admin_id, now_date)

    db = database()
    result = db.select(query)
    db.close()
    if result is None:
        return 'false'
    import ConvertData
    result = ConvertData.ConvertData().convert_to_json(result)
    return result


def get_next_competitions(info):
    admin_id = int(info[0])
    now_date = get_date()

    query = """
        select tbl_competition.name, tbl_competition.date_start, tbl_game.name from tbl_competition
        join tbl_game
        on tbl_competition.id_game=tbl_game.id
        where tbl_competition.admin_id=%d
        and tbl_competition.date_start > '%s'
        order by tbl_competition.date_start
    """ % (admin_id, now_date)

    db = database()
    result = db.select(query)
    db.close()
    if result is None:
        return 'false'
    import ConvertData
    result = ConvertData.ConvertData().convert_to_json(result)
    return result


def add_player(info):
    competition_id = int(info[0])
    player_id = int(info[1])
    competition_type = int(info[2])

    query = ""

    if competition_type == 2:
        query = """select id from tbl_tournament_player
                    where id_user=%d and id_tournament=(select id from tbl_tournament
                    where id_competition=%d
                    limit 1)""" % (player_id, competition_id)
    elif competition_type == 1:
        query = """select id from tbl_league_player
            where id_user=%d and id_league=(select id from tbl_league
            where id_competition=%d
            limit 1)""" % (player_id, competition_id)

    db = database()
    result = db.insert(query)
    db.close()
    if len(str(result).strip()) != 0:
        return 'duplicate'

    if competition_type == 2:
        # Tournament
        query = """
            insert into tbl_tournament_player
            (id_user, id_tournament, status)
            values
            (%d, (select id from tbl_tournament
            where id_competition=%d
            limit 1),
            -1)
        """ % (player_id, competition_id)
    elif competition_type == 1:
        # League
        query = """
            insert into tbl_league_player
            (id_user, id_league, status)
            values
            (%d, (select id from tbl_league
            where id_competition=%d
            limit 1),
            -1)
        """ % (player_id, competition_id)

    db = database()
    result = db.insert(query)
    db.close()
    if result is None:
        return 'false'
    if result:
        return 'true'
    else:
        return 'false'
