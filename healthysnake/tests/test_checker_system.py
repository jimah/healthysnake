from healthysnake.checkers.system import MemoryUtilisationCheck


class TestMemoryUtilisationCheck(object):
    """
    Tests the MemoryUtilisationCheck checker
    """
    def test_initialization(self):
        """
        The checker should use sensible defaults
        """
        checker = MemoryUtilisationCheck()
        assert checker.failure_threshold == 80.0

    def test_checker_success(self, mocker):
        """
        The checker should return True if the memory usage is below the failure threshold
        """
        disk_usage = mocker.Mock(attributes=['percent'])
        disk_usage.percent = 79.0
        mocker.patch('psutil.virtual_memory', mocker.Mock(return_value=disk_usage))
        check = MemoryUtilisationCheck()
        assert check() is True

    def test_checker_failure(self, mocker):
        """
        The checker should return False if the memory usage is above the failure threshold
        """
        disk_usage = mocker.Mock(attributes=['percent'])
        disk_usage.percent = 81.0
        mocker.patch('psutil.virtual_memory', mocker.Mock(return_value=disk_usage))
        check = MemoryUtilisationCheck()
        assert check() == (False, 'currently sitting at 81.0% memory consumption')
