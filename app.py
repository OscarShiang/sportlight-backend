from flask import Flask, request, jsonify
from flask_restful import reqparse
from os import getenv

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
