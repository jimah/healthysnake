import os

from healthysnake import healthcheck, levels
from healthysnake.alerts.slack.manager import SlackAlertManager
from healthysnake.checkers import redis, system

hc = healthcheck.HealthCheck('example_application',
                             alert_managers=[SlackAlertManager(
                                 webhook=os.environ['SLACK_WEBHOOK'],
                             )])


def custom_dependency_check():
    # chosen by fair dice roll
    roll = 4
    return (roll == 4, '')


# hc.add_dependency('soft_failure', check_soft_failure, level=levels.SOFT)
hc.add_dependency('redis', redis.check_redis_connection('127.0.0.1'))
hc.add_dependency('disk_space', system.check_filesystem_storage('/dev/disk0s2', failure_threshold=25),
                  level=levels.SOFT)


print(hc.status())
