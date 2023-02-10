#!/usr/bin/env python3

# 1. copy the folder shutdownthumb to your machine
# 2. 'cd' to that folder
# 3. type 'sudo make install'

# The system will now be shutdown if a thumb drive is inserted which is
# labelled (or has a partition labelled) SHUTDOWNPI


import argparse
import pyudev
import subprocess
import datetime


def main():
    ap = argparse.ArgumentParser('Shutdown RPi on detecting thumb drive')

    ap.add_argument(
        '--label', type=str, default='SHUTDOWNPI',
        help='Drive/partition label to provoke shutdown [SHUTDOWNPI]'
    )

    args = ap.parse_args()

    logMsg = "{0} shutting down in response to detection of partition '{1}'"

    context = pyudev.Context()

    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')

    monitor.start()  # workround for https://github.com/pyudev/pyudev/issues/57

    for device in iter(monitor.poll, None):
        if (
            device.device_type in ['disk', 'partition'] and
            device.get('ID_FS_LABEL') == args.label
        ):
            print(
                logMsg.format(
                    datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),
                    args.label
                ), flush=True
            )
            subprocess.call(['/sbin/shutdown -P now'], shell=True)


if __name__ == '__main__':
    main()
