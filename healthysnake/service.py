from datetime import datetime, timedelta

from healthysnake.levels import HARD


class Service(object):

    STATE_HEALTHY = "healthy"
    STATE_UNHEALTHY = "unhealthy"

    DEFAULT_INTERVAL = 10

    def __init__(self, name, check, interval=timedelta(seconds=DEFAULT_INTERVAL), level=HARD):
        self.name = name
        self.last_updated = datetime.utcnow()
        self.level = level

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
