from datetime import timedelta

from healthysnake import levels
from healthysnake.service import Service


def success_check():
    return True


class TestServiceInitialisation(object):
    def test_defaults(self):
        srv = Service('sherlock', success_check)
        assert srv.name == 'sherlock'
        assert srv._check == success_check
        assert srv._healthy is True
        assert srv.level == levels.HARD
        assert srv._interval == timedelta(seconds=Service.DEFAULT_INTERVAL)

    def test_str(self):
        srv = Service('sherlock', success_check)
        stringified = str(srv)
        assert stringified == 'sherlock [state=healthy, level=1]'

    def test_state_str(self):
        srv = Service('sherlock', success_check)
        assert srv._state_str() == Service.STATE_HEALTHY
        srv._healthy = False
        assert srv._state_str() == Service.STATE_UNHEALTHY

    def test_due(self):
        srv = Service('sherlock', success_check)
        assert srv.due() is False
        srv.last_updated = srv.last_updated - timedelta(seconds=60)
        assert srv.due() is True

    def test_healthy(self):
        srv = Service('sherlock', success_check)
        srv._healthy = False
        assert srv.healthy() is False
        srv.last_updated = srv.last_updated - timedelta(seconds=60)
        assert srv.healthy() is True




