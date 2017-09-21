from .exceptions import ImproperlyConfiguredError


class AbstractAlerterManager:
    """Base AlertManager class to subclass."""

    def alert(self, message):
        """Core alerting mechanism.

        :param message:
        :type message:

        :raises .exceptions.ImproperlyConfiguredError when not implemented by parent class
        """
        raise ImproperlyConfiguredError('alert function not implemented')

    def on_failure(self, exc):
        pass

    def on_success(self, data):
        pass
