from Database import database
from ConvertData import ConvertData


def get_games_list():
    query = """
        select id, name from tbl_game
    """
    db = database()
    result = db.select(query)
    db.close()

    result = ConvertData().convert_to_json(result)
    return result
