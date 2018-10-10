from Database import database


def get_ranking(info):
    game_id = int(info[0])
    city_id = int(info[1])

    query = """
        select tbl_ranking.id, tbl_user.name, tbl_ranking.rank from tbl_ranking
        join tbl_user
        on tbl_user.id=tbl_ranking.user_id
        where tbl_ranking.game_id=%d
        order by tbl_ranking.rank desc
        limit 20
    """ % (game_id)

    db = database()
    result = db.select(query)
    db.close()
    if result is None:
        return 'false'
    import ConvertData
    result = ConvertData.ConvertData().convert_to_json(result)
    return result
