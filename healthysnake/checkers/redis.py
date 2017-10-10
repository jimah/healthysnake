import redis


class RedisConnectionPingable:
    """Checker for ensuring that redis is up and a connection is possible."""

    def __init__(self, host, port=6379, db=0, auth=None):
        """Initialise a new RedisConnectionPingable."""
        self.host = host
        self.port = port
        self.db = db
        self.auth = auth

    def __call__(self):
        """Connect to redis using the details from the initialiser."""
        try:
            r = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.auth,
            )
            return r.ping()
        except redis.ConnectionError:
            return False, 'cannot connect to redis'
        except Exception as e:
            return False, e
        return False, 'an uncaught exception caused RedisConnectionPingable to fail'
