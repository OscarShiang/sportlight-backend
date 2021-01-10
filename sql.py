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

    def getUserByID(self, uID):
        query = f'''SELECT * FROM account WHERE id = '{uID}';'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def createEvent(self, founder, event_info):
        sport, start_at, pos = event_info

        start_at = dt.datetime.strptime(start_at, '%Y-%m-%d %H:%M')
        start_at = dt.datetime.timestamp(start_at)

        query = f'''INSERT INTO event (founder, sport, start_at, created_at, pos) VALUES ('{founder}',
                '{sport}', {psycopg2.TimestampFromTicks(start_at)}, {psycopg2.TimestampFromTicks(time.time())});'''
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def getEvents(self):
        query = f'''SELECT id, founder, sport, participant, start_at, pos FROM event ORDER BY start_at DESC LIMIT 10;'''

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def joinEvent(self, event_id, user_id):
        query = f'''SELECT participant FROM event WHERE id = {event_id};'''
        self.cursor.execute(query)

        participants = self.cursor.fetchone()[0]
        if participants == '':
            participants = str(user_id)
        else:
            participants += f',{user_id}'

        query = f'''UPDATE event SET participant = '{participants}' WHERE id = {event_id}'''
        self.cursor.execute(query)
        self.conn.commit()

        return True

    def insertCGAResult(self, result):
        uid, height, weight, score = result

        query = f'''INSERT INTO cga_result (id, height, weight, score) VALUES ({uid}, {height}, {weight}, {score});'''
        self.cursor.execute(query)
        self.conn.commit()

        return True

    def getCGAResult(self, uid):
        query = f'''SELECT * FROM cga_result WHERE id = {uid};'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
        self.cursor.close()