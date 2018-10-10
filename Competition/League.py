from random import shuffle
from datetime import datetime
from datetime import timedelta
from Database import database
from ConvertData import ConvertData


class League(object):
    def __init__(self):
        pass

    def round_robin(self, units, sets=None):
        """ Generates a schedule of "fair" pairings from a list of units """
        count = len(units)
        sets = sets or (count - 1)
        half = int(count / 2)
        final = list()
        for turn in range(sets):
            left = units[:half]
            right = units[count - half - 1 + 1:][::-1]
            pairings = zip(left, right)
            if turn % 2 == 1:
                pairings = [(y, x) for (x, y) in pairings]
            units.insert(1, units.pop())
            final.append(pairings)
        return final

    def get_schedule(self, teams=['a', 'b', 'c', 'd']):
        shuffle(teams)
        data = self.round_robin(teams, sets=len(teams) * 2 - 2)
        info = list()
        for i in data:
            if type(i) is zip:
                for j in i:
                    info.append(j)
            else:
                for j in i:
                    info.append(j)
        info = self.round_robin_schulde(info)
        return info

    def round_robin_schulde(self, data):

        start_date = datetime.now()
        pm_am = 'pm'

        if pm_am == 'pm':
            hour = 18
        elif pm_am == 'am':
            hour = 8

        info = list()
        counter = 0
        for index, d in enumerate(data):
            date = start_date + timedelta(days=counter)
            date = date.replace(hour=hour + index % 4, minute=0, second=0, microsecond=0)
            if index % 4 == 0:
                counter += 1
            info.append((d[0], d[1], str(date)))
        return info


def get_available_leagues():
    query = """
        select tbl_league.id, tbl_competition.name from tbl_competition
        join tbl_league
        on tbl_competition.id=tbl_league.id_competition
    """
    db = database()
    result = db.select(query)
    db.close()
    result = ConvertData().convert_to_json(result)
    return result

