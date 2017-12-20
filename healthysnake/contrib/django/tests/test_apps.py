from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from healthysnake.healthcheck import HealthCheck


class DummyAlertManager:
    """
    Dummy alert manager class
    """
    def __call__(self, *args, **kwargs):
        pass


class DummyDependency:
    """
    Dummy dependency class
    """
    def __call__(self, *args, **kwargs):
        pass


class TestAppConfig(object):
    """
    Tests the AppConfig
    """
    def test_health_checker(self):
        """
        The app config should have a health checker instance stored against it
        """
        app_config = apps.get_app_config('healthysnake')
        assert isinstance(app_config.health_checker, HealthCheck)

    def test_health_checker_name_from_settings(self):
        """
        The health checker should take it's name from the django settings
        """
        settings.HEALTHY_SNAKE_APP_NAME = 'some-service'

        app_config = apps.get_app_config('healthysnake')
        app_config.ready()

        assert app_config.health_checker.name == 'some-service'

    def test_health_checker_name_from_host(self, mocker):
        """
        The health checker should take it's name from the host
        """
        del settings.HEALTHY_SNAKE_APP_NAME

        mock = mocker.Mock(return_value='myhostname')
        mocker.patch('healthysnake.contrib.django.apps.socket.gethostname', mock)

        app_config = apps.get_app_config('healthysnake')
        app_config.ready()

        assert app_config.health_checker.name == 'myhostname'

    def test_alert_managers(self, mocker):
        """
        The health checker should use the correct alert managers
        """
        mock = mocker.Mock(return_value=[DummyAlertManager()])
        mocker.patch('healthysnake.contrib.django.apps.HealthySnakeConfig._health_checker_alert_managers', mock)

        app_config = apps.get_app_config('healthysnake')
        app_config.ready()

        assert len(app_config.health_checker._alert_managers) == 1
        assert isinstance(app_config.health_checker._alert_managers[0], DummyAlertManager)

    def test_dependencies(self, mocker):
        """
        The health checker should use the correct dependencies
        """
        mock = mocker.Mock(return_value={'dependency_1': DummyDependency()})
        mocker.patch('healthysnake.contrib.django.apps.HealthySnakeConfig._health_checker_dependencies', mock)

        app_config = apps.get_app_config('healthysnake')
        app_config.ready()

        assert len(app_config.health_checker._services.keys()) == 1
        assert isinstance(app_config.health_checker._services['dependency_1']._check, DummyDependency)

    def test_ready_raises_improperly_configured(self, mocker):
        """
        The ready method should raise an ImproperlyConfigured exception
        """
        mock = mocker.Mock(return_value={'dependency_1': 'not-a-callable'})
        mocker.patch('healthysnake.contrib.django.apps.HealthySnakeConfig._health_checker_dependencies', mock)

        app_config = apps.get_app_config('healthysnake')

        try:
            app_config.ready()
        except ImproperlyConfigured:
            pass
        else:
            assert False, "app config ready method did not raise improperly configured exeption"
