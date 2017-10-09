import redis


def check_redis_connection(host, port=6379, db=0, auth=None):
    def callback():
        try:
            r = redis.StrictRedis(
                host=host,
                port=port,
                db=db,
                password=auth,
            )
            return r.ping()
        except redis.ConnectionError:
            return False, 'cannot connect to redis'
        except Exception as e:
            return False, e
    return callback
