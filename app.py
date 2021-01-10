from flask import Flask, request, jsonify
from flask_restful import reqparse
from os import getenv
import datetime as dt

from sql import Database

app = Flask(__name__)
database = Database()

@app.route('/api/account/signup', methods=['POST'])
def signUp():
    parser = reqparse.RequestParser()
    parser.add_argument('user', type=str, required=True, help='Parameter not sufficient')
    parser.add_argument('passwd', type=str, required=True, help='Parameter not sufficient')

    data = parser.parse_args()
    test = database.getAccountInfo(data['user'])
    if test:
        return jsonify({'status': False})

    database.createAccount((data['user'], data['passwd']))
    info = database.getAccountInfo(data['user'])
    res = {
        'status': True,
        'info': {
            'id': info[0],
            'user': info[1]
        }
    }
    return jsonify(res)

@app.route('/api/account/signin', methods=['POST'])
def signIn():
    parser = reqparse.RequestParser()
    parser.add_argument('user', type=str, required=True, help='Parameter not sufficient')
    parser.add_argument('passwd', type=str, required=True, help='Parameter not sufficient')

    data = parser.parse_args()
    info = database.getAccountInfo(data['user'])

    if info and data['passwd'] == info[2]:
        res = {
            'id': info[0],
            'user': info[1]
        }
        return jsonify(res)

    return jsonify(None)

@app.route('/api/account/<int:uid>', methods=['GET'])
def getUser(uid):
    user = database.getUserByID(uid)

    if user:
        res = {
            'id': user[0],
            'user': user[1]
        }
        return jsonify(res)
    
    return jsonify(None)

@app.route('/api/event', methods=['GET'])
def eventGet():
    data_list = database.getEvents()
    event_list = []
    for uid, founder, sport, participant, start_at, pos in data_list:
        date_str = start_at.strftime('%Y-%m-%d %H:%M')
        element = {
            'id': uid,
            'founder': founder,
            'sport': sport,
            'participant': participant,
            'start_at': date_str,
            'pos': pos
        }
        event_list.append(element)

    return jsonify({'events': event_list})

@app.route('/api/event', methods=['POST'])
def eventCreate():
    parser = reqparse.RequestParser()
    parser.add_argument('founder', type=str, required=True)
    parser.add_argument('sport', type=str, required=True)
    parser.add_argument('start_at', type=str, required=True)
    parser.add_argument('pos', type=str, required=True)

    data = parser.parse_args()

    ret = database.createEvent(data['founder'], (data['sport'], data['start_at'], data['pos']))
    return jsonify(ret)

@app.route('/api/event/join', methods=['POST'])
def eventJoin():
    parser = reqparse.RequestParser()
    parser.add_argument('event_id', type=int, required=True)
    parser.add_argument('user_id', type=int, required=True)

    data = parser.parse_args()

    ret = database.joinEvent(data['event_id'], data['user_id'])
    return jsonify(ret)

@app.route('/api/cga/<int:uid>', methods=['GET'])
def getCGAResult(uid):
    data = database.getCGAResult(uid)

    res = {
        'id': data[0],
        'height': data[1],
        'weight': data[2],
        'score': data[3]
    }
    return jsonify(res)

@app.route('/api/cga', methods=['POST'])
def setCGAResult():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('height', type=int, required=True)
    parser.add_argument('weight', type=int, required=True)
    parser.add_argument('score', type=int, required=True)

    data = parser.parse_args()

    result = (data['id'], data['height'], data['weight'], data['score'])
    ret = database.insertCGAResult(result)

    return jsonify(ret)

@app.route('/api/test', methods=['GET', 'POST'])
def test():
    data = {
        'name': 'Hello',
        'phrase': 'world'
    }

    return jsonify(data)

if __name__ == '__main__':
    port = int(getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
