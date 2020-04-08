import pickle
import time
import os

from skyfield.api import Loader

from camera import SatelliteTracker
from predict_passes import get_moon_pos

load = Loader('./data/')
ts = load.timescale()

ROOT_DIR = os.environ['ROOT_DIR']
DATA_DIR = os.path.join(ROOT_DIR, 'data') 
IMAGE_OUTPUT_DIR = os.environ['IMAGE_OUTPUT_DIR']


class Runner:
    def __init__(self, mock):
        self.sat_tracker = SatelliteTracker()
        self.passes = pickle.load(open(os.path.join(DATA_DIR, 'passes.pkl'), 'rb'))
        self.mock = mock

        if not mock:
            self.sat_tracker.mount_init()

    def run_jog(self):
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
                axis = self.sat_tracker.mount.RA_CHANNEL 
            elif d == 'e':
                axis = self.sat_tracker.mount.DEC_CHANNEL
            self.sat_tracker.mount.move_relative(axis=axis, value=v, use_degrees=True)
            
    def run_moon_test(self):
        file_path = os.path.join(IMAGE_OUTPUT_DIR, 'calibration_image.jpg') 
        return self.sat_tracker.take_pictures(file_path, 2, 1)

    def run_observations(self):

        # sort sat passes
        sat_passes = sorted(self.passes, key=lambda p: p[1].tt)

        while(True):
            # filter out past passes
            current = ts.now()
            sat_passes = filter(lambda a: a[1].tt > current.tt, sat_passes)

            try:
                next_sat = next(sat_passes)
            except StopIteration:
                print("All observations complete")
                return

            sat_name, t_obs, (el, az, _) = next_sat
            print("Running observation: {}".format(sat_name))
            self.observe(az, el, t_obs, self.sat_tracker)

    def observe(self, az, el, t_obs):

        if self.mock:
            time.sleep(0.2)

        else:
            self.sat_tracker.move_to_then_shoot(
                    az.degrees,
                    el.degrees,
                    t_obs,
                    margin=1,
                    exposure=6,
                    output_dir=IMAGE_OUTPUT_DIR)


def main(mock, moon_test=True):
    runner = Runner(mock)

    print("Calibrate position")
    do_jog = input("Need to jog? (y/n): ")
    if do_jog == 'y':
        runner.run_jog()
    elif do_jog == 'n':
        pass
    else:
        print("Invalid input")
        exit(1)

    if not mock:
        ra = float(input("Please enter current RA: "))
        dec = float(input("Please enter current dec: "))
        runner.sat_tracker.calibrate(ra, dec)
        
    runner.run_observations()


if __name__ == '__main__':
    main()
