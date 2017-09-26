import subprocess


DF_SIZE_COL = 1
DF_USED_COL = 2
DF_CAPACITY_COL = 4


def check_filesystem_storage(disk, failure_threshold=90):
    def callback():
        df = subprocess.Popen(['df', '-g', '-h'], stdout=subprocess.PIPE)
        output = df.communicate()
        if len(output) == 0:
            # TODO something went wrong
            return False
        decoded = output[0].decode('utf-8')
        lines = decoded.split('\n')

        # get the line that matches the disk
        target = next(line for line in lines if line.startswith(disk))
        trimmed = [col for col in target.split(' ') if col]

        capacity = trimmed[DF_CAPACITY_COL]
        # TODO add these to a message passed back to the healthcheck
        # size = trimmed[DF_SIZE_COL]
        # used = trimmed[DF_USED_COL]
        capacity_perc = capacity[:-1]
        if failure_threshold > int(capacity_perc):
            return False

        return True

    return callback
