import psycopg2
import time
import datetime as dt
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
        query = f'''SELECT * FROM account WHERE name = '{user}';'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def createEvent(self, founder, event_info):
        sport, start_at = event_info

        start_at = dt.datetime.strptime(start_at, '%Y-%m-%d %H:%M')
        start_at = dt.datetime.timestamp(start_at)

        query = f'''INSERT INTO event (founder, sport, start_at, created_at) VALUES ('{founder}',
                '{sport}', {psycopg2.TimestampFromTicks(start_at)}, {psycopg2.TimestampFromTicks(time.time())});'''
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def getEvents(self):
        query = f'''SELECT id, founder, sport, start_at FROM event ORDER BY start_at DESC LIMIT 10;'''

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insertCGAResult(self, result):
        uid, height, weight, ab_wei, exercise, fall_down = result

        query = f'''INSERT INTO cga_result (id, height, weight, abnormal_weight, exercise, fall_down) VALUES ({uid}, {height}, {weight}, {ab_wei}, {exercise}, {fall_down});'''
        self.cursor.execute(query)
        self.conn.commit()

        return True

    def getCGAResult(self, uid):
        query = f'''SELECT height, weight, abnormal_weight, exercise, fall_down FROM cga_result;'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
        self.cursor.close()