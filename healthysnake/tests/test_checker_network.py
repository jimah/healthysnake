from requests.exceptions import SSLError

from healthysnake.checkers.network import HTTPAddressReachable


def success_check():
    return True


class TestHTTPAddressReachable(object):
    """
    Tests the HTTPAddressReachable checker
    """
    def test_initialization(self):
        """
        The checker should use sensible defaults
        """
        checker = HTTPAddressReachable('http://example.com')
        assert checker.address == 'http://example.com'
        assert checker.expected_status_code == 200

    def test_checker_success(self, mocker):
        """
        The checker should return True if returned status code matches the expected status code
        """
        response = mocker.Mock(attributes=['status_code'])
        response.status_code = 200
        mocker.patch('requests.get', mocker.Mock(return_value=response))

        check = HTTPAddressReachable('http://example.com')
        assert check() is True

    def test_checker_failure(self, mocker):
        """
        The checker should return False if returned status code does not match the expected status code
        """
        response = mocker.Mock(attributes=['status_code'])
        response.status_code = 500
        mocker.patch('requests.get', mocker.Mock(return_value=response))

        check = HTTPAddressReachable('http://example.com')
        assert check() is False

    def test_checker_ssl_failure(self, mocker):
        """
        The checker should return False if returned status code does not match the expected status code
        """
        mocker.patch('requests.get', mocker.Mock(side_effect=SSLError))

        check = HTTPAddressReachable('http://example.com')
        assert check() == (False, 'http://example.com has failed to verify the SSL certificate')
