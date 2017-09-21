import os

from healthysnake import healthcheck, levels
from healthysnake.alerts.slack.manager import SlackAlertManager

hc = healthcheck.HealthCheck('example_application',
                             alert_managers=[SlackAlertManager(
                                 webhook=os.environ['SLACK_WEBHOOK'],
                             )])


def check_success():
    # chosen by fair dice roll
    roll = 4
    return roll == 4

hc.add_dependency('success', check_success)


def check_soft_failure():
    roll = 2
    return roll == 4


hc.add_dependency('soft_failure', check_soft_failure, level=levels.SOFT)

print(hc.status())
