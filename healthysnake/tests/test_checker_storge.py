from healthysnake.checkers.storage import DiskCapacityCheck


class TestDiskCapacityCheck(object):
    """
    Tests the DiskCapacityCheck checker
    """
    def test_initialization(self):
        """
        The checker should use sensible defaults
        """
        checker = DiskCapacityCheck('/media')
        assert checker.mountpoint == '/media'
        assert checker.failure_threshold == 90.0

    def test_checker_success(self, mocker):
        """
        The checker should return True if the storage has not filled up beyond the specified threshold
        """
        disk_usage = mocker.Mock(attributes=['percent'])
        disk_usage.percent = 89.0
        mocker.patch('psutil.disk_usage', mocker.Mock(return_value=disk_usage))
        check = DiskCapacityCheck('/media')
        assert check() is True

    def test_checker_failure(self, mocker):
        """
        The checker should return False if the storage has filled up beyond the specified threshold
        """
        disk_usage = mocker.Mock(attributes=['percent'])
        disk_usage.percent = 91.0
        mocker.patch('psutil.disk_usage', mocker.Mock(return_value=disk_usage))
        check = DiskCapacityCheck('/media')
        assert check() == (False, 'mount point "/media" reached 91.0% capacity')
