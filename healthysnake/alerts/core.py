from .exceptions import ImproperlyConfiguredError


class Alert:
    """The core alert data model, contains information to be passed to a manager."""

    def __init__(self, application, dependency, message, severity, metadata=None, source='localhost'):
        """Create a new Alert.

        :param message: string data to be sent to the alert manager
        :type message: str

        :param severity: healthysnake level indicating severity of alert
        :type severity: int

        :param metadata: optional dictionary of metadata to send
        :type metadata: dict
        """
        if metadata is None:
            metadata = {}

        self.application = application
        self.dependency = dependency
        self.message = message
        self.severity = severity
        self.metadata = metadata
        self.source = source


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
