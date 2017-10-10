import requests


class HTTPAddressReachable:
    """Checker for ensuring that a HTTP address is reachable.

    If the address provided is prefixed with "https" this checker with also ensure SSL validity.
    """

    def __init__(self, address, expected_status_code=200):
        """Initialise a new HTTPAddressReachable."""
        self.address = address
        self.expected_status_code = expected_status_code

    def __call__(self):
        """Hit the request URL, check the status code against what is expected."""
        try:
            r = requests.get(self.address)
        except requests.exceptions.SSLError:
            return False, '{0} has failed to verify the SSL certificate'.format(self.address)
        return r.status_code == self.expected_status_code
