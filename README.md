# healthysnake

[![CircleCI](https://circleci.com/gh/dammitjim/healthysnake.svg?style=svg)](https://circleci.com/gh/dammitjim/healthysnake)

healthysnake is a flexible levels-based monitoring library for your application's network dependencies. It is intended
as a first step towards improved visibility in your applications before committing to a more intensive monitoring
solution.

Currently, healthysnake is in development and should be used in production systems at your own risk.

## Levels

Applications may have both hard dependencies which are required for the app to continue running and soft which allow
the app to continue with degraded service.

All times are in UTC.

## Installation

```bash
    pip install healthysnake
```
(when it gets onto pip hopefully)

## Example usage

```python
import os

from healthysnake import healthcheck, levels
from healthysnake.alerts.slack.manager import SlackAlertManager
from healthysnake.checkers import redis, storage, system, network

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

```

## Example Output

```javascript
    {
        'name':'example_application',
        'healthy':True,
        'dependencies':[
            {
                'healthy':True,
                'next_update':1505987207.0,
                'last_updated':1505987197.0,
                'level':2,
                'name':'success'
            },
            {
                'healthy':False,
                'next_update':1505987207.0,
                'last_updated':1505987197.0,
                'level':1,
                'name':'soft_failure'
            }
        ]
    }
```

## Alerts

healthysnake currently supports the following alerting systems:

* Slack
    - `pip install requests` tested at 2.18.4
* TODO Sentry
* TODO Email
