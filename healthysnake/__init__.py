from time import mktime, sleep
from datetime import datetime, timedelta


class Service(object):

    LEVEL_HARD = "hard"
    LEVEL_SOFT = "soft"

    STATE_HEALTHY = "healthy"
    STATE_UNHEALTHY = "unhealthy"

    DEFAULT_INTERVAL = 10

    def __init__(self, name, check, interval=timedelta(seconds=DEFAULT_INTERVAL), severity=LEVEL_HARD):
        self.name = name
        self.last_updated = datetime.utcnow()
        self.level = severity

        self._check = check
        self._interval = interval
        self._healthy = True

        self.update()

    def __str__(self):
        return "{name} [state={state}, level={level}]!".format(
            name=self.name, state=self._state_str(), level=self.level)

    def _state_str(self):
        return self.STATE_HEALTHY if self._healthy else self.STATE_UNHEALTHY

    def update(self):
        self._healthy = bool(self._check())
        self.last_updated = datetime.utcnow()

    def healthy(self):
        if self.due():
            self.update()
        return self._healthy

    def due(self):
        return datetime.utcnow() > self.next_update()

    def next_update(self):
        return self.last_updated + self._interval


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


if __name__ == "__main__":
    hc = HealthCheck('main_service')


    def force_healthy():
        return True

    def force_unhealthy():
        return False

    hc.add_dependency('dependency1', force_healthy)
    hc.add_dependency('dependency2', force_healthy)
    hc.add_dependency('dependency3', force_unhealthy, severity=levels.SOFT)

    hc.status()
    while True:
        sleep(2)
        print(hc.status())


