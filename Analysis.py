from Database import database
from ConvertData import ConvertData
import Food
import Rent
import Game
from Competition import Competition
from Competition import Tournament, League
from Enum.Enums import enum_competition_type
import Administration
import Player
import Tools
import Rank

no_query = 'no query'
spliter = ':!!:'


class Analysis(object):
    def __init__(self):
        pass

    def analysis(self, data):
        if data.startswith(no_query):
            tmp = data.split(spliter)
            if tmp[1] == 'orderfood':
                result = Food.order_food(tmp[2:])
                return result
            elif tmp[1] == 'foodreports':
                result = Food.get_foot_orders(tmp[2:])
                return result
            elif tmp[1] == 'rent':
                result = Rent.analysis(tmp[2:])
                return result
            elif tmp[1] == 'get games list':
                result = Game.get_games_list()
                return result
            elif tmp[1] == 'login':
                result = Administration.login(tmp[2:])
                return result
            elif tmp[1] == 'slider':
                result = Tools.get_sliders()
                return result
            elif tmp[1] == 'signup':
                if tmp[2] == 'level 1':
                    result = Player.signup_level_1(tmp[3:])
                elif tmp[2] == 'level 2':
                    result = Player.signup_level_2(tmp[3:])
                return result
            elif tmp[1] == 'player':
                if tmp[2] == 'get next game':
                    result = Player.get_next_game(tmp[3])
                    return result

            elif tmp[1] == 'tournament':
                if tmp[2] == 'check for start pre':
                    result = Tournament.check_for_start_pre(tmp[3])
                    return result
                elif tmp[2] == 'get playing':
                    result = Tournament.get_paying(tmp[3])
                    return result

            elif tmp[1] == 'admin':
                if tmp[2] == 'get admins':
                    result = Administration.get_admins_list(tmp[3:])
                    return result
                elif tmp[2] == 'get admin description':
                    result = Administration.get_admin_description(tmp[3:])
                    return result

            elif tmp[1] == 'rank':
                if tmp[2] == 'get ranking':
                    result = Rank.get_ranking(tmp[3:])
                    return result

            # Competitions
            elif tmp[1] == 'competition':
                if tmp[2] == 'get games list':
                    result = Competition.get_games_list()
                    return result
                elif tmp[2] == 'add player':
                    result = Competition.add_player(tmp[3:])
                    return result
                elif tmp[2] == 'get next competition':
                    result = Competition.get_next_competition(tmp[3:])
                    return result
                elif tmp[2] == 'get next competitions':
                    result = Competition.get_next_competitions(tmp[3:])
                    return result
                elif tmp[2] == 'get competition info':
                    result = Competition.get_competition_info(tmp[3:])
                    return result
                elif tmp[2] == 'new competition':
                    result = Competition.new_competition(tmp[3:])
                    return result
                elif tmp[2] == 'get available tournaments':
                    result = Tournament.get_available_tournaments()
                    return result
                elif tmp[2] == 'get available leagues':
                    result = League.get_available_leagues()
                    return result
                elif tmp[2] == 'signup to competition':
                    if tmp[3] == 'league':
                        type = enum_competition_type.League
                        result = Competition.signup_to_competition_by_cardid(type)
                        return result
                    elif tmp[3] == 'tournament':
                        type = enum_competition_type.Tournament
                        result = Competition.signup_to_competition_by_cardid(tmp[4:], type)
                        return result
        else:
            query = data
            db = database()
            if query.lower().startswith('insert'):
                result = db.insert(query)
            elif query.lower().startswith('update'):
                result = db.update(query)
            elif query.lower().startswith('delete'):
                result = db.delete(query)
            else:
                result = db.select(query)
                result = ConvertData().convert_to_json(result)
            return result
