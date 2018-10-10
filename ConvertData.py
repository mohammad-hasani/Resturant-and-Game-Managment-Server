import json
import datetime

class ConvertData(object):
    def __init__(self):
        pass

    def convert_to_json(self, data):
        if data == None:
            return
        if len(data) == 0:
            return
        tmp = [list(item) for item in data]
        for index1, i in enumerate(tmp):
            for index2, j in enumerate(i):
                if isinstance(j, datetime.datetime):
                    tmp[index1][index2] = str(tmp[index1][index2])
        converted_data = json.dumps(tmp)
        return converted_data

    def convert_from_json(self, data):
        return json.loads(data)

