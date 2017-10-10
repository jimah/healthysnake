import os

from healthysnake import healthcheck, levels
from healthysnake.alerts.slack.manager import SlackAlertManager
from healthysnake.checkers import network, redis, storage, system

hc = healthcheck.HealthCheck('example_application',
                             alert_managers=[SlackAlertManager(
                                 webhook=os.environ['SLACK_WEBHOOK'],
                             )])


# checkers can be defined as simple functions
def custom_functional_dependency_check():
    # chosen by fair dice roll
    roll = 4
    return (roll == 4, '')


hc.add_dependency('CUSTOM_FUNCTIONAL_CHECK', custom_functional_dependency_check, level=levels.SOFT)


# or they can be defined as a callable object
class CustomClassBasedCheck:
    def __call__(self):
        # chosen by fair dice roll
        roll = 4
        return (roll == 4, '')


hc.add_dependency('CUSTOM_CLASS_BASED_CHECK', CustomClassBasedCheck(), level=levels.SOFT)

# healthysnake also comes with a variety of useful checkers out of the box
hc.add_dependency('REDIS', redis.RedisConnectionPingable('127.0.0.1'))
hc.add_dependency('DISK SPACE', storage.DiskCapacityCheck('/', failure_threshold=90.0),
                  level=levels.SOFT)
hc.add_dependency('RAM', system.MemoryUtilisationCheck(failure_threshold=75.0))
hc.add_dependency('NETWORK_DEPENDENCY', network.HTTPAddressReachable("https://dammitjim.co.uk"))

print(hc.status())
