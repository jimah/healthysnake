import os
import json

import requests

from healthysnake.alerts.core import AbstractAlerterManager


class SlackAlertManager(AbstractAlerterManager):

    def __init__(self, webhook):
        self.webhook_url = webhook

    def alert(self, message):
        self._send_to_webhook({
            'text': message,
        })

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
