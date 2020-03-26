import pickle
import time
import os

from skyfield.api import Loader

from camera import SatelliteTracker

load = Loader('./data/')

ROOT_DIR = os.environ['ROOT_DIR']
DATA_DIR = os.path.join(ROOT_DIR, 'data') 


def run_jog(mount):
    print("Welcoming to the jogging interface!")
    print("Use this to position the camera in a known \
            orientation for calibration")
    while True:
        d = input("enter axis [a, e] or any other key to exit: ").lower()
        if d in 'ae':
            try:
                v = int(input("enter steps to jog (int): "))
            except ValueError:
                print("not a valid int")
                continue
        else:
            print("jogging complete - hope you had fun!")
            return
        if d == 'a':
            axis = mount.RA_CHANNEL 
        elif d == 'e':
            axis = mount.DEC_CHANNEL
        mount.move_relative(axis=axis, value=v, use_degrees=False)
        
          

def run_observations(camera, passes, time_scale, mock):

    # sort sat passes
    sat_passes = sorted(passes, key=lambda p: p[1].tt)


    while(True):
        # filter out past passes
        current = time_scale.now()
        sat_passes = filter(lambda a: a[1].tt > current.tt, sat_passes)

        try:
            next_sat = next(sat_passes)
        except StopIteration:
            print("All observations complete")
            return

        observe(next_sat, camera, mock)


def observe(sat, camera, mock):
    sat_name, t_obs, (dec, ra, _) = sat

    if mock:
        time.sleep(0.2)

    else:
        #TODO: implement this section
        # check_some_shit()
        # move_the_camera()
        camera.move_to_then_shoot(ra.degrees, dec.degrees, t_obs, margin=1, exposure=10, output_dir='./output_images')
    print("Running observation: {}".format(sat))


def main(mock=False):
    ts = load.timescale()
    passes = pickle.load(open(os.path.join(DATA_DIR, 'passes.pkl'), 'rb'))
    camera = SatelliteTracker()

    # TODO jarmg: change to a camera init
    if not mock:
        camera.mount_init()

    print("Calibrate position")
    do_jog = input("Need to jog? (y/n): ")
    if do_jog == 'y':
        run_jog(camera.mount)
    elif do_jog == 'n':
        pass
    else:
        print("Invalid input")
        exit(1)

    if not mock:
        ra = float(input("Please enter current RA: "))
        dec = float(input("Please enter current dec: "))
        camera.calibrate(ra, dec)
        
    run_observations(camera, passes, ts, mock)


if __name__ == '__main__':
    main()
