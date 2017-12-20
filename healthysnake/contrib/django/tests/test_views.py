import json

from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.test import RequestFactory

from healthysnake.contrib.django.views import HealthCheckView


class TestHealthCheckView:
    """
    Tests the HealthCheckView
    """
    url = reverse_lazy('healthy_snake:health_check_view')

    @staticmethod
    def _get_view():
        """
        Helper method for creating and returning the view instance for testing
        """
        view = HealthCheckView()
        view.request = RequestFactory().get('/fake-path/')
        return view

    def test_renders(self, mocker):
        """
        The view should render
        """
        mock = mocker.Mock(return_value={'foo': 'bar'})
        mocker.patch('healthysnake.contrib.django.views.HealthCheckView.get_health_status', mock)

        response = self._get_view().get(self.url)
        decoded_content = response.content.decode("utf-8")
        json_data = json.loads(decoded_content)

        assert response.status_code == 200
        assert isinstance(response, JsonResponse)
        assert len(json_data.keys()) == 1
        assert json_data['foo'] == 'bar'

    def test_get_health_checker(self, mocker):
        """
        The method should return the health checker for the correct app
        """
        app_config = mocker.Mock()
        app_config.health_checker = mocker.Mock()

        mock = mocker.Mock(return_value=app_config)
        mocker.patch('healthysnake.contrib.django.views.apps.get_app_config', mock)

        checker = self._get_view().get_health_checker()

        mock.assert_called_with('healthysnake')
        assert checker == app_config.health_checker

    def test_get_health_status(self, mocker):
        """
        The get_health_status method should return the correct data
        """
        checker = mocker.Mock()
        checker.status = mocker.Mock(return_value={'foo': 'bar'})
        mocker.patch(
            'healthysnake.contrib.django.views.HealthCheckView.get_health_checker',
            mocker.Mock(return_value=checker)
        )

        status = self._get_view().get_health_status()

        assert len(status.keys()) == 1
        assert status['foo'] == 'bar'
