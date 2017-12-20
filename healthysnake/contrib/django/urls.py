from django.conf.urls import url

from healthysnake.contrib.django.views import HealthCheckView


urlpatterns = [url(r'^$', HealthCheckView.as_view(), name='health_check_view')]
