import psutil


class MemoryUtilisationCheck:
    """Check to ensure utilised memory is within the given threshold (monitor for OOM)."""

    def __init__(self, failure_threshold=80.0):
        """Initialise a new MemoryUtilisationCheck."""
        self.failure_threshold = failure_threshold

    def __call__(self):
        """Get the virtual memory, check against the failure threshold."""
        vmem = psutil.virtual_memory()
        return vmem.percent < self.failure_threshold, 'currently sitting at {0}% memory consumption'.format(
            vmem.percent,
        )
