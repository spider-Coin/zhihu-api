from __future__ import absolute_import, unicode_literals

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cache import Cache
from flask_pymongo import PyMongo
from flask_cors import CORS
import pymongo
import logging


app = Flask(__name__)
CORS(app, origins=["https://togetthere.cn/",
                   "http://localhost:8080"])
app.config.from_pyfile('config.py')
api = Api(app)
mongo = PyMongo(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


parser1 = reqparse.RequestParser()
parser1.add_argument('text', location='json', required=True)


class Inlian(Resource):
    def post(self):
        args = parser1.parse_args()
        text = args['text']
        text = text.strip()

        def run(text, nonce=None):
            try:
                tx = playGame(text, nonce=nonce)
                return {'tx': tx, 'ok': 1}
            except ValueError:
                nonce = int(getredis())+1
                return run(text, nonce)
            except:
                logging.exception('...')
            return {'msg': '系统错误,请重试', 'ok': 0}
        return run(text)


api.add_resource(Inlian, '/write')


if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=True)
