from healthysnake.alerts.manager import AbstractAlerterManager
import healthysnake.levels as levels

from ..manager import SlackAlertManager


class TestSlackAlertManager:
    def test_initialisation(self):
        wanted_webhook = 'testerino'
        sam = SlackAlertManager(webhook=wanted_webhook)
        assert sam.webhook_url == wanted_webhook
        assert isinstance(sam, AbstractAlerterManager)

    def test_color_from_severity(self):
        testcases = [
            (levels.SOFT, SlackAlertManager.SLACK_COLOR_WARNING),
            (levels.HARD, SlackAlertManager.SLACK_COLOR_DANGER),
            (None, SlackAlertManager.SLACK_COLOR_GOOD),
        ]
        for testcase in testcases:
            assert SlackAlertManager.slack_color_from_level(testcase[0]) == testcase[1]

    def test_how_many_fires(self):
        testcases = [
            (levels.SOFT, 1),
            (levels.HARD, 2),
            (None, 0),
        ]
        for testcase in testcases:
            assert SlackAlertManager.how_many_fires(testcase[0]).count(
                SlackAlertManager.SLACK_FIRE_EMOJI) == testcase[1]
