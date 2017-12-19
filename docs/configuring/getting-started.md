# Getting started

## Requirements

Healthysnake officially supports Python 3, Python 2 support is pending work.

## Installation

Healthysnake is available on pip:

```bash
pip install healthysnake
```

## The Healthcheck object

All of Healthysnake revolves around a core healthcheck object, this is what keeps track of your dependencies, invokes
checks and initiates alerts. To start using Healthysnake, you'll need to create a new healthcheck:

```python
from healthysnake import healthcheck

# creates a new HealthCheck object with the name of "my_application"
hc = healthcheck.HealthCheck('my_application')
```

### Adding dependencies

From here, you will need to add dependencies to the healthcheck. A dependency contains a callable object referred to as
a "checker". A checker can be any callable that returns a tuple of format (bool, message).

```python
def check_my_math():
    return (2 + 2) == 4, ''

hc.add_dependency('MY MATH', check_my_math)
```

The boolean returned indicates whether or not the dependency has passed the check. The message is tertiary information
that could be useful off the back of the result.

Checker functions may also be class based.

```python
class CheckMyMath:
    def __call__(self):
        return (2 + 2) == 4, ''

hc.add_dependency('MY MATH', CheckMyMath())
```

### Levels

A dependency has an associated severity level. Currently Healthysnake supports two levels; HARD and SOFT. When a HARD
dependency fails it's check, the entire status registers as unhealthy. On the other hand, if a SOFT dependency fails it's check
the status remains as healthy with the individual dependency registering as unhealthy.

Alerters can be configured to  
