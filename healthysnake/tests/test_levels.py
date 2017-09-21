import healthysnake.levels as levels


class TestLevels:
    def test_level_as_string(self):
        assert levels.level_as_string(levels.HARD) == 'HARD'
        assert levels.level_as_string(levels.SOFT) == 'SOFT'
