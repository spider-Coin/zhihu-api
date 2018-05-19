from __future__ import absolute_import, unicode_literals

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cache import Cache
from flask_pymongo import PyMongo
from flask_cors import CORS
import pymongo
import logging
import json


app = Flask(__name__)
CORS(app, origins=["https://togetthere.cn/",
                   "http://localhost:8080"])
app.config.from_pyfile('config.py')
api = Api(app)
mongo = PyMongo(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


parser = reqparse.RequestParser()
parser.add_argument('url', location='json', required=True)
parser.add_argument('data', location='json', required=True)


class Task(Resource):
    def post(self):
        args = parser.parse_args()
        data = json.loads(args.data)
        save2db(data, args.url)

    def get(self):
        return {'url': ['https://www.zhihu.com/api/v4/members/pa-chong-21/activities?limit=7&after_id=1525849360&desktop=True'],
                'status': 'ok',
                'ifNext': False}


def save2db(data, url):
    if isinstance(data, list):
        for i in data:
            i['source_url'] = url
            mongo.db.user.insert_one(i)
    else:
        data['source_url'] = url
        mongo.db.user.insert_one(i)


api.add_resource(Task, '/task')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=False)
