from time import sleep
from datetime import datetime, timedelta


class Service(object):
    DEFAULT_INTERVAL = 10

    def __init__(self, name, check, interval=timedelta(0, DEFAULT_INTERVAL)):
        self.name = name
        self.last_update = datetime.now()

        self._check = check
        self._interval = interval
        self._healthy = True

        self.update()

    def __str__(self):
        return "{name} is {state}!".format(name=self.name, state=self._state_str())

    def _state_str(self):
        if self._healthy:
            return "healthy"
        return "unhealthy"

    def update(self):
        self._healthy = bool(self._check())
        self.last_update = datetime.now()

    def healthy(self):
        if self.due():
            self.update()
        return self._healthy

    def due(self):
        return datetime.now() > self.next_update()

    def next_update(self):
        return self.last_update + self._interval


class HealthCheck(object):

    _dependencies = []

    def __init__(self):
        # TODO allow multiple checks passed in
        pass

    def add_check(self, check_func):
        # TODO add a new health check
        pass

    def render(self):
        # TODO render the health check
        pass

hc = HealthCheck()


def test_service():
    return True

srv = Service("pipeline", test_service)
