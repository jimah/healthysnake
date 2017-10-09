# Built in checkers

## Redis

Alert when redis is unable to connect

### Requirements

```bash
pip install redis
```

### Usage

```python
from healthysnake.checkers import redis

# initialise your healthcheck
hc = healthcheck.HealthCheck(...)

hc.add_dependency('redis', redis.check_redis_connection('127.0.0.1', auth='PASSWORD'))
```

## Disk Usage

Alert when disk usage breaches a percentage threshold

### Usage

```python
from healthysnake.checkers import system

# initialise your healthcheck
hc = healthcheck.HealthCheck(...)

# if the disk usage % is greater than 70%, fail.
hc.add_dependency('/dev/yourdisk', system.check_filesystem_storage('/dev/yourdisk', failure_threshold=70))
```
