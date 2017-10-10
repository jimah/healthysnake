import psutil


class DiskCapacityCheck:
    """Checker for ensuring that disk capacity is within the specified limit."""

    def __init__(self, mountpoint, failure_threshold=90.0):
        """Initialise a new DiskCapacityCheck."""
        self.mountpoint = mountpoint
        self.failure_threshold = failure_threshold

    def __call__(self):
        """Check the disk usage for the given mountpoint against the failure threshold."""
        disk_usage = psutil.disk_usage(self.mountpoint)
        return disk_usage.percent < self.failure_threshold, 'mount point "{0}" reached {1}% capacity'.format(
            self.mountpoint,
            disk_usage.percent,
        )
