import logging
from time import mktime
from datetime import timedelta

from healthysnake import exceptions, levels
from healthysnake.dependency import Dependency
from healthysnake.alerts.core import Alert


class HealthCheck:
    """
    Tracks the state of all dependencies.
    """

    def __init__(self, name,
                 logger=logging.getLogger(__name__),
                 alert_managers=None,
                 ):
        """
        :param name: the name of the service running the health check
        :type name: str

        :param logger: optional logger, defaults to root logger
        :type logger: logging.Logger
        """
        self.name = name
        self.healthy = True
        self.dependencies = {}

        self._logger = logger
        self._services = {}

        if alert_managers is None:
            alert_managers = []
        self._alert_managers = alert_managers

    def __str__(self):
        return self.status()

    def add_dependency(self, name, check_func,
                       interval=timedelta(seconds=Dependency.DEFAULT_INTERVAL), level=levels.HARD):
        """
        Add a dependency to be tracked within the health check.

        :param name: name of the dependency
        :type name: str

        :param check_func: callback function to be run to check the health of a dependency
        :type check_func: callable

        :param interval: how often it should be checked
        :type interval: datetime.timedelta

        :param level: severity level for dependency
        :type level: int
        """
        if name in self._services:
            raise exceptions.DependencyAlreadyPresentException(name + ' already present in health check')

        srv = Dependency(name, check_func, interval, level)
        self._services[name] = srv

    def check_dependency(self, name):
        """
        Check that the specified dependency is healthy

        :param name: the name of the dependency
        :type name: str

        :return: result of health check
        :rtype: bool
        """
        if name not in self._services.keys():
            raise exceptions.DependencyNotPresentException(name + ' not present in health check dependencies')

        return self._services[name].healthy()

    def status(self):
        """
        Generate a dictionary representing the current health state of the system.

        :return: dictionary representation of system state
        :rtype: {}
        """
        tracked_dependencies = []
        for name, dependency in self._services.items():
            dependency_healthy = (False, '')
            try:
                dependency_healthy = dependency.healthy()
            except Exception as e:
                self._logger.exception(e)

            if not dependency_healthy[0]:
                for manager in self._alert_managers:
                    # TODO name the check that failed
                    manager.alert(Alert(
                        application=self.name,
                        dependency=name,
                        message=dependency_healthy[1],
                        severity=dependency.level,
                    ))

            tracked_dependencies.append({
                'name': name,
                'healthy': dependency_healthy[0],
                'level': dependency.level,
                'last_updated': mktime(dependency.last_updated.timetuple()),
                'next_update': mktime(dependency.next_update().timetuple()),
            })

        # golf so hard pythonistas wanna fine me
        self.healthy = all(d['healthy'] for d in tracked_dependencies if d['level'] != levels.SOFT)

        return {
            'name': self.name,
            'healthy': self.healthy,
            'dependencies': tracked_dependencies,
        }
