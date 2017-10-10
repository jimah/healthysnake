import psutil


def check_memory_utilisation(failure_threshold=80.0):
    """Check that the memory utilisation of the system falls under the failure threshold."""
    def callback():
        vmem = psutil.virtual_memory()
        return vmem.percent < failure_threshold, 'currently sitting at {0}% memory consumption'.format(vmem.percent)
    return callback
