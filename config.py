from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'app.upLastime',
        'schedule': timedelta(seconds=60 * 30)
    }
}
MONGO_URI = 'mongodb://127.0.0.1:27017/zhihu'
CELERY_BROKER_URL = 'redis://localhost:6379',
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 1
