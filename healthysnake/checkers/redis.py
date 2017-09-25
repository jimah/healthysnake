import os

import redis


def check_redis_connection():
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = os.environ.get('REDIS_PORT', 6380)
    redis_db = os.environ.get('REDIS_DB', 0)
    try:
        r = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            db=redis_db
        )
        return r.ping()
    except redis.ConnectionError:
        print('cant connect to redis')
    except Exception as e:
        print(e)
    return False
