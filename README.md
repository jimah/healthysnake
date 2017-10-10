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
    from datetime import timedelta
    from healthysnake import healthcheck, levels

    # initialise the health check for your application
    hc = healthcheck.HealthCheck('your_application_name')

    # health check functions simply need to return true or false
    def check_redis_health():
        # check you can connect to redis
        return True

    # add the dependency
    hc.add_dependency('redis', check_redis_health)

    def check_postgres_health():
        # check you can connect to postgres
        return True

    # optionally add a specific interval, defaults to 1 minute
    hc.add_dependency('postgresql', check_postgres_health, interval=timedelta(seconds=120))

    def check_external_service_health():
        return True

    # for non vital services, you can mark them as a "soft" dependency, one that your app can continue
    # without
    hc.add_dependency('non_vital_service', check_external_service_health, level=levels.SOFT)
```

## Example Output

```json
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
