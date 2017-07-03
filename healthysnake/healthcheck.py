from time import mktime
from datetime import timedelta

from healthysnake import exceptions, levels
from healthysnake.service import Service


class HealthCheck(object):

    dependencies = {}
    healthy = True

    _services = {}

    def __init__(self, name):
        self.name = name

    def add_dependency(self, name, check_func,
                       interval=timedelta(seconds=Service.DEFAULT_INTERVAL), level=levels.HARD):
        if name in self._services:
            raise exceptions.DependencyAlreadyPresentException(name + ' already present in health check')
        srv = Service(name, check_func, interval, level)
        self._services[name] = srv

    def check_dependency(self, name):
        if name not in self._services:
            raise exceptions.DependencyNotPresentException(name + ' not present in health check dependencies')
        return self._services[name].healthy()

    def status(self):
        healthy = True
        dependencies = []
        for name, dependency in self._services.items():
            if not dependency.healthy() and dependency.level == levels.HARD:
                healthy = False

            dependencies.append({
                'name': name,
                'healthy': healthy,
                'level': dependency.level,
                'last_updated': mktime(dependency.last_updated.timetuple()),
                'next_update': mktime(dependency.next_update().timetuple()),
            })

        self.healthy = healthy

        return {
            'name': self.name,
            'healthy': self.healthy,
            'dependencies': dependencies,
        }
