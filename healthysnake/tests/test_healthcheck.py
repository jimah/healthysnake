import logging
from datetime import datetime, timedelta
from freezegun import freeze_time
from time import mktime

import pytest

from healthysnake import exceptions, levels
from healthysnake.healthcheck import HealthCheck


def success_check():
    return True


def fail_check():
    return False


def fail_check_with_message():
    return False, 'The check failed'


def exception_check():
    raise Exception('bang')


class TestHealthCheck(object):
    """
    Tests the HealthCheck class
    """
    def test_init(self):
        """
        The HealthCheck constructor should set up the instance correctly
        """
        logger = logging.getLogger(__name__)
        hc = HealthCheck('app', logger=logger)
        assert hc.name == 'app'
        assert hc._logger is not None
        assert hc.healthy is True
        assert hc._alert_managers == []

    def test_add_dependency(self):
        """
        The add_dependency method should add the dependency to the apps services.
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency', success_check, interval=timedelta(seconds=60), level=levels.SOFT)
        assert hc._services['dependency'] is not None
        assert hc._services['dependency']._interval == timedelta(seconds=60)
        assert hc._services['dependency'].level == levels.SOFT

    def test_add_dependency_raises_exception(self):
        """
        The method should raise an exception if the dependency name conflicts with an existing dependency
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency', success_check, interval=timedelta(seconds=60), level=levels.SOFT)
        with pytest.raises(exceptions.DependencyAlreadyPresentException):
            hc.add_dependency('dependency', success_check, interval=timedelta(seconds=60), level=levels.SOFT)

    def test_check_dependency(self):
        """
        The method should raise an exception if the dependency does not exist
        """
        hc = HealthCheck('app')
        with pytest.raises(exceptions.DependencyNotPresentException):
            hc.check_dependency('dependency')

    def test_check_dependency_valid(self):
        """
        The method should return a tuple containing the healthy status and failure message
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency', success_check)
        assert hc.check_dependency('dependency') == (True, '')

    def test_check_dependency_invalid(self):
        """
        The method should return a tuple containing the healthy status and empty failure message
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency', fail_check)
        assert hc.check_dependency('dependency') == (False, '')

    def test_check_dependency_invalid_with_message(self):
        """
        The method should return a tuple containing the healthy status and failure message
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency', fail_check_with_message)
        assert hc.check_dependency('dependency') == (False, 'The check failed')

    @freeze_time('2017-1-1 12:00:00')
    def test_status_success(self):
        """
        The HealthCheck status method should return a dict containing:

         - The app name;
         - Whether the app is healthy or not;
         - A list of all dependency statuses, each including:
           - The dependency name;
           - Whether the dependency is healthy or not;
           - The failure level;
           - A unix timestamp identifying when the dependency was last checked;
           - A unix timestamp identifying when the dependency should be checked next;
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        status = hc.status()
        assert status['name'] == 'app'
        assert status['healthy'] is True
        # Check the dependencies
        dep = status['dependencies'][0]
        assert dep['name'] == 'dependency1'
        assert dep['healthy'] is True
        assert dep['level'] is levels.HARD
        last_updated = dep['last_updated']
        assert last_updated <= mktime(datetime.utcnow().timetuple())
        assert dep['next_update'] == last_updated + 10

    def test_status_success_soft_failing(self):
        """
        The app should still report itself as healthy if a dependency fails with a soft failure
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        hc.add_dependency('dependency2', fail_check, level=levels.SOFT)
        status = hc.status()
        assert status['healthy'] is True
        soft_dep = next(dep for dep in status['dependencies'] if dep['level'] == levels.SOFT)
        assert soft_dep['healthy'] is False

    def test_status_unhealthy_hard_failing(self):
        """
        The app status should report itself as not healthy if any of its dependencies fail hard
        """
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        hc.add_dependency('dependency2', fail_check)
        status = hc.status()
        assert status['healthy'] is False

    def test_status_raise_exception_counts_as_fail(self):
        """
        If a dependency raises n exception it should be treated as a hard failure
        """
        logging.disable(logging.CRITICAL)
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        hc.add_dependency('dependency2', exception_check)
        hc._services['dependency2'].last_updated = hc._services['dependency2'].last_updated - timedelta(seconds=60)
        status = hc.status()
        assert status['healthy'] is False
