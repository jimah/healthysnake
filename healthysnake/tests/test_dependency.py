from datetime import timedelta
from freezegun import freeze_time

from healthysnake import levels
from healthysnake.dependency import Dependency


def success_check():
    return True


class TestDependencyInitialisation(object):
    """
    Tests initialization of the dependency class
    """
    def test_defaults(self):
        """
        The dependency should be initialized with appropriate default values
        """
        srv = Dependency('sherlock', success_check)
        assert srv.name == 'sherlock'
        assert srv._check == success_check
        assert srv._healthy is True
        assert srv.level == levels.HARD
        assert srv._interval == timedelta(seconds=Dependency.DEFAULT_INTERVAL)

    def test_str(self):
        """
        The string representation of the dependency should return the dependency name, state and failure level
        """
        srv = Dependency('sherlock', success_check)
        stringified = str(srv)
        assert stringified == 'sherlock [state=healthy, level=2]'

    def test_state_str(self):
        """
        The method should return the appropriate value depending on the value of the _healthy attribute
        """
        srv = Dependency('sherlock', success_check)
        assert srv._state_str() == Dependency.STATE_HEALTHY
        srv._healthy = False
        assert srv._state_str() == Dependency.STATE_UNHEALTHY

    @freeze_time('2017-1-1 12:00:00')
    def test_due(self):
        """
        The method should return False if checked within last <interval> seconds, otherwise True
        """
        srv = Dependency('sherlock', success_check)
        assert srv.due() is False
        srv.last_updated = srv.last_updated - timedelta(seconds=60)
        assert srv.due() is True

    def test_healthy(self):
        """
        The method should identify whether the dependency is healthy or not
        """
        srv = Dependency('sherlock', success_check)
        srv._healthy = False
        assert srv.healthy() == (False, '')
        srv.last_updated = srv.last_updated - timedelta(seconds=60)
        assert srv.healthy() == (True, '')
