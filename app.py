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
        return jsonify(False)

    database.createAccount((data['user'], data['passwd']))
    return jsonify(True)

@app.route('/api/account/signin', methods=['POST'])
def signIn():
    parser = reqparse.RequestParser()
    parser.add_argument('user', type=str, required=True, help='Parameter not sufficient')
    parser.add_argument('passwd', type=str, required=True, help='Parameter not sufficient')

    data = parser.parse_args()
    info = database.getAccountInfo(data['user'])

    if info and data['passwd'] == info[1]:
        return jsonify(True)

    return jsonify(False)

@app.route('/api/event', methods=['GET'])
def eventGet():
    data_list = database.getEvents()
    event_list = []
    for founder, sport, start_at in data_list:
        date_str = start_at.strftime('%Y-%m-%d %H:%M')
        element = {
            'founder': founder,
            'sport': sport,
            'start_at': date_str
        }
        event_list.append(element)

    return jsonify({'events': event_list})

@app.route('/api/event', methods=['POST'])
def eventCreate():
    parser = reqparse.RequestParser()
    parser.add_argument('founder', type=str, required=True)
    parser.add_argument('sport', type=str, required=True)
    parser.add_argument('start_at', type=str, required=True)

    data = parser.parse_args()

    ret = database.createEvent(data['founder'], (data['sport'], data['start_at']))
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
    app.run(host='0.0.0.0', port=port, debug=True)
