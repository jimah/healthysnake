import subprocess


def check_filesystem_storage(failure_threshold, warning_threshold=None):
    def _check_filesystem_storage():
        df = subprocess.Popen(['df'], stdout=subprocess.PIPE)
        output = df.communicate()[0]
        return False
    return _check_filesystem_storage
