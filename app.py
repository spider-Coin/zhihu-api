from __future__ import absolute_import, unicode_literals

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cache import Cache
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_redis import FlaskRedis

import pymongo
import logging
import json


app = Flask(__name__)
CORS(app, origins=["*"])
app.config.from_pyfile('config.py')
api = Api(app)
mongo = PyMongo(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
redis_store = FlaskRedis(app)


parser = reqparse.RequestParser()
parser.add_argument('url', location='json', required=True)
parser.add_argument('data', location='json', required=True)


class Task(Resource):
    def post(self):
        args = parser.parse_args()
        data = json.loads(args.data)
        save2db(data, args.url)

    def get(self):
        try:
            ret = redis_store.lpop('urls')
            if ret:
                ret = ret.decode('utf8')
                return (json.loads(ret))

            else:
                return {'status': 'ok', 'url': ''}
        except Exception as e:
            return {'status': '', 'msg': str(e)}


class Feed(Resource):
    def get(self, id):
        return [i['target'] for i in mongo.db.feed.find({'verb': 'QUESTION_FOLLOW'}).limit(10)]


def save2db(data, url):
    if isinstance(data, list):
        for i in data:
            i['source_url'] = url
            mongo.db.user.insert_one(i)
    else:
        data['source_url'] = url
        mongo.db.user.insert_one(i)


def getLastTime(url_token):
    # 返回某个人最新动态的时间
    xx = mongo.db.user.find({'actor.url_token': url_token}, {
        'created_time': 1, '_id': 0}).sort([("created_time", -1)]).limit(1)
    return xx['created_time']


api.add_resource(Task, '/api/task')
api.add_resource(Feed, '/api/feed/<string:id>')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000, threaded=False)
