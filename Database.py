import MySQLdb


class database():
    def __init__(self, host='localhost', username='root', password='admin', dbname='nutrica'):
        self.opendatabase(host, username, password, dbname)

    def opendatabase(self, host, username, password, dbname):
        self.db = MySQLdb.connect(host, username, password, dbname)
        self.db.set_character_set('utf8')
        self.cursor = self.db.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def select(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        if len(data) > 0:
            return data
        else:
            return None

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def update(self, query):
        try:
            self.cursor.execute(query)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def delete(self, query):
        try:
            self.cursor.execute(query)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def callproc(self, name, args, query):
        self.cursor.callproc(name, args)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.cursor.close()
        self.db.close()
