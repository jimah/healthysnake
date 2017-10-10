import requests


def check_address_reachable(address, expected_status_code=200):
    def callback():
        try:
            r = requests.get(address)
        except requests.exceptions.SSLError:
            return False, '{0} has failed to verify the SSL certificate'.format(address)
        return r.status_code == expected_status_code
    return callback
