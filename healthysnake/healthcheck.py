import logging
from time import mktime
from datetime import timedelta

from healthysnake import exceptions, levels
from healthysnake.service import Service


class HealthCheck:

    def __init__(self, name, logger=None):
        self.name = name
        self._logger = logger
        self._services = {}
        self.healthy = True
        self.dependencies = {}

    def add_dependency(self, name, check_func,
                       interval=timedelta(seconds=Service.DEFAULT_INTERVAL), level=levels.HARD):
        if name in self._services:
            raise exceptions.DependencyAlreadyPresentException(name + ' already present in health check')
        srv = Service(name, check_func, interval, level)
        self._services[name] = srv

    def check_dependency(self, name):
        if name not in self._services.keys():
            raise exceptions.DependencyNotPresentException(name + ' not present in health check dependencies')
        return self._services[name].healthy()

    def status(self):
        dependencies = []
        for name, dependency in self._services.items():
            dependency_healthy = False

            try:
                dependency_healthy = dependency.healthy()
            except Exception as e:
                # TODO figure out the best way of doing this
                if self._logger:
                    self._logger.exception(e)
                else:
                    logging.getLogger(__name__).exception(e)

            dependencies.append({
                'name': name,
                'healthy': dependency_healthy,
                'level': dependency.level,
                'last_updated': mktime(dependency.last_updated.timetuple()),
                'next_update': mktime(dependency.next_update().timetuple()),
            })

        # golf so hard pythonistas wanna fine me
        self.healthy = all(d['healthy'] for d in dependencies if d['level'] != levels.SOFT)

        return {
            'name': self.name,
            'healthy': self.healthy,
            'dependencies': dependencies,
        }
