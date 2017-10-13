from redis import ConnectionError

from healthysnake.checkers.redis import RedisConnectionPingable


def success_check():
    return True


class TestRedisConnectionPingable(object):
    """
    Tests the RedisConnectionPingable checker
    """
    def test_initialization(self):
        """
        The checker should use sensible defaults
        """
        checker = RedisConnectionPingable('127.0.0.1')
        assert checker.host == '127.0.0.1'
        assert checker.port == 6379
        assert checker.db == 0
        assert checker.auth is None

    def test_redis_client_initialization(self, mocker):
        """
        The redis client should be initialized with the correct data
        """
        mock = mocker.Mock(return_value=None)
        mocker.patch('redis.StrictRedis.__init__', mock)
        check = RedisConnectionPingable(
            '127.0.0.1',
            port=1234,
            db=1,
            auth='auth-string'
        )
        check()
        mock.assert_called_with(
            host='127.0.0.1',
            port=1234,
            db=1,
            password='auth-string'
        )

    def test_checker_success(self, mocker):
        """
        The checker should return True if redis ping returns a response
        """
        mocker.patch('redis.StrictRedis.ping', mocker.Mock(return_value=True))
        check = RedisConnectionPingable('127.0.0.1')
        assert check() is True

    def test_checker_failure(self, mocker):
        """
        The checker should return False if redis ping does not return a response
        """
        mocker.patch('redis.StrictRedis.ping', mocker.Mock(return_value=False))
        check = RedisConnectionPingable('127.0.0.1')
        assert check() is False

    def test_checker_connection_error(self, mocker):
        """
        The checker should return False if could not connect to redis
        """
        mocker.patch('redis.StrictRedis.ping', mocker.Mock(side_effect=ConnectionError))
        check = RedisConnectionPingable('127.0.0.1')
        assert check() == (False, 'cannot connect to redis')

    def test_checker_broad_exception(self, mocker):
        """
        The checker should return False if an exception is raised
        """
        mocker.patch('redis.StrictRedis.ping', mocker.Mock(side_effect=Exception))
        check = RedisConnectionPingable('127.0.0.1')
        assert check() == (False, 'an uncaught exception caused RedisConnectionPingable to fail')
