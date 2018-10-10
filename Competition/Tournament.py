import random
from Database import database
from ConvertData import ConvertData
from Enum.Enums import enum_competition_type


class Tournament(object):
    def __init__(self):
        pass

    def single_elimination(self, teams):
        random.shuffle(teams)
        len_teams = len(teams)
        data = list()
        for i in range(0, len_teams, 2):
            if i + 1 == len_teams:
                data.append((teams[i],))
            else:
                data.append((teams[i], teams[i + 1]))
        return data


def get_available_tournaments():
    query = """
            select tbl_tournament.id, tbl_competition.name from tbl_competition
            join tbl_tournament
            on tbl_competition.id=tbl_tournament.id_competition
        """
    db = database()
    result = db.select(query)
    db.close()
    result = ConvertData().convert_to_json(result)
    return result


def check_for_start_pre(admin_id):
    admin_id = int(admin_id)
    query = """
        select tbl_tournament.id from tbl_tournament
        join tbl_competition
        on tbl_tournament.id_competition=tbl_competition.id
        where admin_id=%d
    """ % (admin_id)
    db = database()
    result = db.select(query)
    db.close()
    check_for_start(result)


def check_for_start(tournament_id):
    for i in tournament_id:
        db = database()
        tmp_tournament_id = int(i[0])
        args = [tmp_tournament_id, 0]
        query = 'select @_tournament_check_start_1'
        result = db.callproc('tournament_check_start', args, query)[0][0]
        db.close()
        if result == 0:
            pass
        else:
            start(tournament_id)


def start(tournament_id):
    tournament_id = int(tournament_id)
    query = """
            select id_user from tbl_tournament_player
            where id_tournament=%d
            """ % (tournament_id)
    db = database()
    result = db.select(query)
    db.close()

    teams = [team for team in result[0]]
    teams = Tournament().single_elimination(teams)

    for i in teams:
        query = """
            insert into tbl_tournament_playing
            (id_tournament)
            values
            (%d)
        """ % (tournament_id)

        db = database()
        result = db.insert(query)
        tournament_playing_id = \
            db.select(
                'select id from tbl_tournament_playing where id_tournament=%d order by id DESC ' % (tournament_id))[
                0][0]
        tournament_playing_id = int(tournament_playing_id)
        db.close()

        for j in range(2):
            query = """
                insert into tbl_tournament_playing_user
                (id_user, id_tournament_playing)
                values
                (%d, %d)
            """ % (int(i[j]), tournament_playing_id)

            db = database()
            result = db.insert(query)
            db.close()
    return True


def check_for_next_round(tournament_id):
    pass


def next_round(tournament_id):
    query = """
        select name, id_game, count, date_signup, date_start from tbl_competition
        join tbl_tournament
        on
        tbl_tournament.id_competition=tbl_competition.id
        where tbl_tournament.id=%d
        limit 1
    """ % (tournament_id)
    db = database()
    data = db.select(query)
    db.close()

    nickname = data[0][0]
    id_game = int(data[0][1])
    competition_type = enum_competition_type.Tournament
    team_count = int(data[0][3])
    signup_date = data[0][4]
    start_date = data[0][5]

    spliter = Analysis.spliter

    data = nickname + spliter + id_game + spliter + competition_type + spliter + team_count + spliter + \
           signup_date + spliter + start_date

    result = Competition.new_competition(data)

    query = """
        select tbl_tournament_playing_user.id_user from tbl_tournament_playing
        join tbl_tournament_playing_user
        on tbl_tournament_playing_user.id_tournament_playing=tbl_tournament_playing.id
        where tbl_tournament_playing.id_tournament=%d
        and
        win=1
    """ % (tournament_id)
    db = database()
    result = db.select(query)
    db.close()

    new_tournament_id = get_last_tournament_id()

    for i in result:
        id_user = int(i[0])
        type = enum_competition_type.Tournament

        data = [id_user, new_tournament_id]

        Competition.signup_to_competition_by_userid(data, type)

    return True


def get_tournament_winners(tournament_id):
    pass


def get_last_tournament_id():
    query = """
        select id from tbl_tournament
        order by id desc
        limit 1
    """
    db = database()
    result = db.select(query)
    result = result[0][0]
    result = int(result)
    return result


def get_paying(admin_id):
    admin_id = int(admin_id)
    query = """
        select tbl_tournament_playing.id, tbl_user.name from tbl_tournament_playing
        join tbl_user
        join tbl_tournament_playing_user
        join tbl_tournament
        join tbl_competition
        on
        tbl_tournament_playing.id_tournament=tbl_tournament.id
        and
        tbl_tournament.id_competition=tbl_competition.id
        and
        tbl_tournament_playing_user.id_tournament_playing=tbl_tournament_playing.id
        and
        tbl_tournament_playing_user.id_user=tbl_user.id
        where
        tbl_competition.admin_id=%d
    """ % (admin_id)

    db = database()
    result = db.select(query)
    db.close()
    result = ConvertData().convert_to_json(result)
    return result
