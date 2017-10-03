import logging
from datetime import datetime, timedelta
from time import mktime

import pytest

from healthysnake import exceptions, levels
from healthysnake.healthcheck import HealthCheck


def success_check():
    return True


def fail_check():
    return False


def exception_check():
    raise Exception('bang')


class TestHealthCheck(object):
    def test_init(self):
        logger = logging.getLogger(__name__)
        hc = HealthCheck('app', logger=logger)
        assert hc.name == 'app'
        assert hc._logger is not None

    def test_add_dependency(self):
        hc = HealthCheck('app')
        hc.add_dependency('dependency', success_check, interval=timedelta(seconds=60), level=levels.SOFT)
        assert hc._services['dependency'] is not None
        assert hc._services['dependency']._interval == timedelta(seconds=60)
        assert hc._services['dependency'].level == levels.SOFT

        with pytest.raises(exceptions.DependencyAlreadyPresentException):
            hc.add_dependency('dependency', success_check, interval=timedelta(seconds=60), level=levels.SOFT)

    def test_check_dependency(self):
        hc = HealthCheck('app')
        with pytest.raises(exceptions.DependencyNotPresentException):
            hc.check_dependency('dependency')
        hc.add_dependency('dependency', success_check)
        assert hc.check_dependency('dependency') == (True, '')

    def test_status_success(self):
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        status = hc.status()
        assert status['name'] == 'app'
        assert status['healthy'] is True
        dep = status['dependencies'][0]
        assert dep['name'] == 'dependency1'
        assert dep['healthy'] is True
        assert dep['level'] is levels.HARD
        last_updated = dep['last_updated']
        assert last_updated <= mktime(datetime.utcnow().timetuple())
        assert dep['next_update'] == last_updated + 10

    def test_status_success_soft_failing(self):
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        hc.add_dependency('dependency2', fail_check, level=levels.SOFT)
        status = hc.status()
        assert status['healthy'] is True
        soft_dep = next(dep for dep in status['dependencies'] if dep['level'] == levels.SOFT)
        assert soft_dep['healthy'] is False

    def test_status_unhealthy_hard_failing(self):
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        hc.add_dependency('dependency2', fail_check)
        status = hc.status()
        assert status['healthy'] is False

    def test_status_raise_exception_counts_as_fail(self):
        logging.disable(logging.CRITICAL)
        hc = HealthCheck('app')
        hc.add_dependency('dependency1', success_check)
        hc.add_dependency('dependency2', exception_check)
        hc._services['dependency2'].last_updated = hc._services['dependency2'].last_updated - timedelta(seconds=60)
        status = hc.status()
        assert status['healthy'] is False
