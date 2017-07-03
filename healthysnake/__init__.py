from time import sleep

from healthysnake.service import Service
from healthysnake.healthcheck import HealthCheck

if __name__ == "__main__":
    hc = HealthCheck('main_service')


    def force_healthy():
        return True

    def force_unhealthy():
        return False

    hc.add_dependency('dependency1', force_healthy)
    hc.add_dependency('dependency2', force_healthy)
    hc.add_dependency('dependency3', force_unhealthy, severity=Service.LEVEL_SOFT)

    hc.status()
    while True:
        sleep(2)
        print(hc.status())


