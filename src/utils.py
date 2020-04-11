import os
from time import time


def run_jog_loop(tracker):
    print("Welcoming to the jogging interface!")
    print("Use this to position the camera in a known \
            orientation for calibration")
    while True:
        d = input("enter axis [a, e] or any other key to exit: ").lower()
        if d in 'ae':
            try:
                v = int(input("enter degrees to jog (int): "))
            except ValueError:
                print("not a valid int")
                continue
        else:
            print("jogging complete - hope you had fun!")
            return
        if d == 'a':
            axis = tracker.mount.RA_CHANNEL
        elif d == 'e':
            axis = tracker.mount.DEC_CHANNEL
        tracker.mount.move_relative(axis=axis, value=v, use_degrees=True)


def is_mount_available():
    # If no ping success for 10 seconds, mount is disconnected
    health_dir = os.environ['HEALTH_DIR']
    assert health_dir is not None

    try:
        f = open(os.path.join(health_dir, 'mount'))
        last_check = int(f.readline())
        now = time()
        return now - last_check < 10

    except IOError:
        return False
