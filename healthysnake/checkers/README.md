# Built in checkers

## Redis

### Requirements

```bash
pip install redis
```

### Ping

Alert when redis is unable to ping

```python
from healthysnake.checkers import redis

# initialise your healthcheck
hc = healthcheck.HealthCheck(...)

hc.add_dependency('REDIS', redis.RedisConnectionPingable('127.0.0.1', auth='PASSWORD'))
```

## Storage

### Disk Capacity

Alert when disk usage breaches a percentage threshold

```python
from healthysnake.checkers import storage

# initialise your healthcheck
hc = healthcheck.HealthCheck(...)

# if the disk usage % is greater than 70%, fail.
hc.add_dependency('DISK SPACE', storage.DiskCapacityCheck('/dev/yourdisk', failure_threshold=70))
```

## System

### Memory Usage

Alert when memory usage breaches the set failure threshold

```python
from healthysnake.checkers import system

# initialise your healthcheck
hc = healthcheck.HealthCheck(...)

hc.add_dependency('RAM', system.MemoryUtilisationCheck(failure_threshold=75.0))
```

## Network

### HTTP Availability

Alert when the given address cannot be reached over http.

SSL check for https addresses.

```python
from healthysnake.checkers import network

# initialise your healthcheck
hc = healthcheck.HealthCheck(...)

hc.add_dependency('NETWORK_DEPENDENCY', network.HTTPAddressReachable("https://dammitjim.co.uk"))
```
