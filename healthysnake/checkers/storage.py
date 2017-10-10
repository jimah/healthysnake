import psutil


def check_remaining_capacity(mountpoint, failure_threshold=90.0):
    def callback():
        disk_usage = psutil.disk_usage(mountpoint)
        return disk_usage.percent < failure_threshold, 'mount point "{0}" reached {1}% capacity'.format(mountpoint, disk_usage.percent)
    return callback
