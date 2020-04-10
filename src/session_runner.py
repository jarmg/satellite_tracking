import pickle
import time
import os
import threading
from datetime import datetime

from skyfield.api import Loader

from camera import SatelliteTracker
from predict_passes import predict_passes, get_moon_pos

from utils import run_jog_loop


load = Loader('./data/')
ts = load.timescale()

ROOT_DIR = os.environ['ROOT_DIR']
DATA_DIR = os.path.join(ROOT_DIR, 'data') 
OUTPUT_DIR = os.environ['IMAGE_OUTPUT_DIR']


class Session:
    def __init__(self):
        self.location = {'lat': '47.647654', 'lon': '-122.324748'}
        self.start_time = datetime.now()
        self.output_dir = os.path.join(
                OUTPUT_DIR,
                self.start_time.strftime("%m-%d-%Y_%H:%M:%S"))
        self.observation_count = 0
        self._passes = [] 

    def _download_passes(self):
        print("downloading passes..")
        passes = predict_passes(**self.location, cache=False)
        self._passes = sorted(passes, key=lambda p: p[1].tt)
        print("finished downloading passes.")

    @property
    def next_pass(self):
        secs_per_day = 24 * 360
        now = ts.now().tt
        p = self.passes.pop(0)
        while (secs_per_day * (p[1].tt - now)) < 10:
            print(p[1].tt - now)
            p = self.passes.pop(0)
        return p

    @property
    def passes(self):
        if len(self._passes) == 0:
            self._download_passes()
        return self._passes

    @property
    def exposure(self):
        return os.environ['EXPOSURE'] 

    def run_observations(self, sat_tracker, stop_event: threading.Event):
        while(not stop_event):
            sat_name, t_obs, (el, az, _) = self.next_pass
            print("Running observation: {}".format(sat_name))

            sat_tracker.move_to(az.degrees, el.degrees)

            margin = 3  # seconds before to start image
            mg_dt = margin / 24 / 60 / 60
            begin = ts.tt_jd(t_obs.tt - mg_dt)

            while begin.tt > ts.now().tt:
                sec_until = (begin.tt - ts.now().tt) * 60 * 60 * 24
                start = begin.utc_strftime('%X')
                print("exposure of {az}, {el} in T-{t_m} secs at {start}"
                      .format(az=az, el=el, t_m=sec_until, start=start))
                time.sleep(1)

            file_name = sat_name + '_' + \
                datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

            sat_tracker.take_pictures(
                   self.output_dir,
                   file_name,
                   self.exposure,
                   1)

def main():
    tracker = SatelliteTracker()
    tracker.mount_init()
    session = Session()

    print("Calibrate position")
    do_jog = input("Need to jog? (y/n): ")
    if do_jog == 'y':
        run_jog_loop(session.sat_tracker)
    elif do_jog == 'n':
        pass
    else:
        print("Invalid input")
        exit(1)

    ra = float(input("Please enter current RA: "))
    dec = float(input("Please enter current dec: "))
 
    tracker.calibrate(ra, dec)
    session.run_observations(tracker)


if __name__ == '__main__':
    main()
