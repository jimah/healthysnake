# What is Healthysnake?

Healthysnake is a flexible, levels-based health monitoring and alerting library for your python applications and systems. 
It can be executed as a script, or integrated with a larger application / framework. It is intended as a first step towards
improved visibility into the running of your systems before making a commitment to a more intensive monitoring solution.

At it's core, Healthysnake accepts a series of "checker" functions which resolve a boolean value as to whether or not
the checker has passed. If the checker returns true it is considered healthy. An example of this could be a ping to an 
external API your application relies on. When Healthysnake's status is invoked, it accumulates the results of these
checker operations and gives an overall picture of system health.

An example of Healthysnake looks like the following:

```python
# TODO
```

This outputs the following dictionary:

```json
{
  "TODO": "TODO"
}
```

Healthysnake aims to remain light and modular, so you can pick and choose what you want to enable.

## Example use cases

You may run a self-hosted piece of software (such as Sentry) which has a dependency on Redis being alive. You could add
Healthysnake to run on a cron job checking the status of Redis and alerting you if it is unable to connect.

You may run a series of network accessible applications that communicate with each other, having Healthysnake ping 
the dependent application health endpoints allows you to assess the health of the communication across them and system
as a whole.

You may have some optional dependencies (such as a seperate thumbnailing service) which, in the event that they are unavailable,
do not stop your application from functioning. In those situations Healthysnake could be used to notify your users that
there may be some degredation in their service.

## Integration into frameworks

Healthysnake currently only supports Django in the core library, with the hope that in the future more frameworks will be
contributed.
