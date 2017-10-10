import os

from healthysnake import healthcheck, levels
from healthysnake.alerts.slack.manager import SlackAlertManager
from healthysnake.checkers import redis, storage, system, network

hc = healthcheck.HealthCheck('example_application',
                             alert_managers=[SlackAlertManager(
                                 webhook=os.environ['SLACK_WEBHOOK'],
                             )])


def custom_dependency_check():
    def callback():
        # chosen by fair dice roll
        roll = 4
        return (roll == 4, '')
    return callback


hc.add_dependency('CUSTOM_CHECK', custom_dependency_check(), level=levels.SOFT)
hc.add_dependency('REDIS', redis.check_redis_connection('127.0.0.1'))
hc.add_dependency('DISK SPACE', storage.check_remaining_capacity('/', failure_threshold=90.0),
                  level=levels.SOFT)
hc.add_dependency('RAM', system.check_memory_utilisation(failure_threshold=75.0))
hc.add_dependency('NETWORK_DEPENDENCY', network.check_address_reachable('https://dammitjim.co.uk'))

print(hc.status())
