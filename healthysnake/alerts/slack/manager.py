import json

import requests

from healthysnake.alerts.manager import AbstractAlerterManager
import healthysnake.levels as levels


class SlackAlertManager(AbstractAlerterManager):

    SLACK_COLOR_GOOD = 'good'
    SLACK_COLOR_DANGER = 'danger'
    SLACK_COLOR_WARNING = 'warning'
    SLACK_FIRE_EMOJI = ':fire:'

    def __init__(self, webhook):
        self.webhook_url = webhook

    def alert(self, alert_message):
        self._send_to_webhook({
            'fallback': 'ALERT {0} failed {1}'.format(alert_message.application, alert_message.dependency),
            'color': self.slack_color_from_level(alert_message.severity),
            'fields': [
                {
                    'title': alert_message.application,
                    'short': True,
                },
                {
                    'title': 'Severity: {0}'.format(levels.level_as_string(alert_message.severity)),
                    'value': self.how_many_fires(alert_message.severity),
                    'short': True,
                },
                {
                    'title': alert_message.dependency,
                    'value': alert_message.message,
                },
            ]
        })

    @staticmethod
    def how_many_fires(severity):
        if not severity:
            return ''

        fires = ''

        end = int(severity)
        i = 0
        while i < end:
            fires += SlackAlertManager.SLACK_FIRE_EMOJI + ' '
            i += 1

        return fires

    @staticmethod
    def slack_color_from_level(severity):
        if severity == levels.SOFT:
            return SlackAlertManager.SLACK_COLOR_WARNING
        elif severity == levels.HARD:
            return SlackAlertManager.SLACK_COLOR_DANGER
        return SlackAlertManager.SLACK_COLOR_GOOD

    def _send_to_webhook(self, payload):
        response = requests.post(
            self.webhook_url,
            data=json.dumps(payload),
            headers={
                'Content-Type': 'application/json',
            },
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
