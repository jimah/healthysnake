import logging
from datetime import timedelta

import pytest

from healthysnake import exceptions, levels
from healthysnake.healthcheck import HealthCheck


def success_check():
    return True


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
        assert hc.check_dependency('dependency') is True


