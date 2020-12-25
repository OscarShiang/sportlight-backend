import psycopg2
from os import getenv

DATABASE_URL = getenv('DATABASE_URL', None)

class Database():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()

    def createAccount(self, info):
        name, passwd = info
        query = f'''INSERT INTO account (name, passwd) VALUES ('{name}', '{passwd}');'''
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def getAccountInfo(self, user):
        query = f'''SELECT name, passwd FROM account WHERE name = '{user}';'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
        self.cursor.close()