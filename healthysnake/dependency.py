import logging
from datetime import datetime, timedelta

from healthysnake.levels import HARD


class Dependency:
    """
    An individual dependency of the system.
    """

    STATE_HEALTHY = 'healthy'
    STATE_UNHEALTHY = 'unhealthy'

    DEFAULT_INTERVAL = 10

    def __init__(self, name, check_func,
                 interval=timedelta(seconds=DEFAULT_INTERVAL), level=HARD, logger=logging.getLogger(__name__)):
        """
        :param name: name of the dependency
        :type name: str

        :param check_func: health check function to update state
        :type check_func: callable

        :param interval: interval by which to update the state
        :type interval: datetime.timedelta

        :param level: severity level of the dependency
        :type level: int

        :param logger: logger for messaging
        :type logger: logging.Logger
        """
        self.name = name
        self.last_updated = datetime.utcnow()
        self.level = level

        self._check = check_func
        self._interval = interval
        self._healthy = True
        self._logger = logger

        self.update()

    def __str__(self):
        """
        :return: string representation of the dependency
        :rtype: str
        """
        return '{name} [state={state}, level={level}]'.format(
            name=self.name, state=self._state_str(), level=self.level)

    def _state_str(self):
        """
        Return appropriate string according to dependency health.

        :return: healthy / unhealthy string const
        :rtype: str
        """
        return self.STATE_HEALTHY if self._healthy else self.STATE_UNHEALTHY

    def update(self):
        """
        Update the health state of the dependency.
        """
        try:
            self._healthy = bool(self._check())
        except Exception as e:
            self._healthy = False
            self._logger.exception(e)

        self.last_updated = datetime.utcnow()

    def healthy(self):
        """
        Retreive the current health of the dependency.

        :return: current health
        :rtype: bool
        """
        if self.due():
            self.update()
        return self._healthy

    def due(self):
        """
        Check whether the dependency is due to update health status.

        :return: true if due to update
        :rtype: bool
        """
        return datetime.utcnow() > self.next_update()

    def next_update(self):
        """
        Calculate the next update time.

        :return: the next update time
        :rtype: datetime.datetime
        """
        return self.last_updated + self._interval
