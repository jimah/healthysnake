from django.conf.urls import url, include


urlpatterns = [
    url(r'^health-check/', include('healthysnake.contrib.django.urls', namespace='healthy_snake')),
]
