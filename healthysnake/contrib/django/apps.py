import socket

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from healthysnake import healthcheck


class HealthySnakeConfig(AppConfig):
    """
    AppConfig for the HealthySnake app
    """
    name = 'healthysnake'
    verbose_name = "healthy snake"
    health_checker = None

    def _health_checker_name(self):
        """
        Generates and returns the name for the health checker

        If the django settings module defines settings.HEALTHY_SNAKE_APP_NAME
        it will be used for the health checker name. If not the servers hostname
        will be used in its place.

        :return: Name for the health checker
        """
        return getattr(settings, 'HEALTHY_SNAKE_APP_NAME', socket.gethostname())

    def _health_checker_alert_managers(self):
        """
        Generates and returns a list of alert managers for the health checker

        Chances are that this may not actually be required when implemented into
        a django project but it is being included for completeness and flexibility

        If the django settings module defines settings.HEALTHY_SNAKE_ALERT_MANAGERS
        it will be used for the health checkers list of alert managers. If not an
        empty list will be used in its place.

        :return: list of alert manager instances
        """
        return getattr(settings, 'HEALTHY_SNAKE_ALERT_MANAGERS', [])

    def _health_checker_dependencies(self):
        """
        Generates and returns a dict of dependency checkers for the health checker

        If the django settings module defines settings.HEALTHY_SNAKE_DEPENDENCIES
        it will be used for the health checkers list of dependencies. If not an
        empty dict will be used in its place.

        :return: dict of dependencies
        """
        return getattr(settings, 'HEALTHY_SNAKE_DEPENDENCIES', {})

    def ready(self):
        """
        Called when the app has finished loading

        Creates a new HealthCheck instance, sets up configured dependencies
        and stores the checker against the app config for later use

        :raise: ImproperlyConfigured
        """
        super().ready()
        self.health_checker = healthcheck.HealthCheck(
            self._health_checker_name(),
            alert_managers=self._health_checker_alert_managers()
        )

        # Loop through all defined dependencies and add each to the HealthChecker in turn
        # Raise an ImproperlyConfigured exception if the dependencies have been misconfigured
        for dependency_name, dependency_checker in self._health_checker_dependencies().items():
            if not callable(dependency_checker):
                raise ImproperlyConfigured(
                    "Expected settings.HEALTHY_SNAKE_DEPENDENCIES['{0}'] "
                    "to be a callable but it was not. Please ensure that "
                    "all values in settings.HEALTHY_SNAKE_DEPENDENCIES are "
                    "callable".format(dependency_name)
                )
            self.health_checker.add_dependency(dependency_name, dependency_checker)
