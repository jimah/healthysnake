from time import mktime
from datetime import timedelta

from healthysnake.service import Service


class HealthCheck(object):

    dependencies = {}
    healthy = True

    _services = {}

    def __init__(self, name):
        # TODO allow multiple checks passed into initialiser
        self.name = name

    def add_dependency(self, name, check_func,
                       interval=timedelta(seconds=Service.DEFAULT_INTERVAL), severity=Service.LEVEL_HARD):
        if name in self._services:
            # TODO proper error
            raise ValueError('already there m8')
        srv = Service(name, check_func, interval, severity)
        self._services[name] = srv

    def check_dependency(self, name):
        if name not in self._services:
            # TODO proper error
            raise ValueError('doesn\'t exist badger')
        return self._services[name].healthy()

    def status(self):
        healthy = True
        dependencies = []
        for name, dependency in self._services.items():
            if not dependency.healthy() and dependency.level == Service.LEVEL_HARD:
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
