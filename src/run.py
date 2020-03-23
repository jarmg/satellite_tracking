import pickle
import time

from skyfield.api import Loader

from camera import SatelliteTracker

load = Loader('./data/')


def jog():
    while True:
        d = input("enter direction to jog [WASD]: ").lower()
        v = int(input("enter steps to jog (int): "))
        if d == 'w':
            print("move up {}".format(v))
        elif d == 's':
            print("move down {}".format(v))
        elif d == 'd':
            print("move right")
        elif d == 'a':
            print("move left")
        elif d == 'x':
            print("exit")
            return 
        else:
            print(d)
          

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
    passes = pickle.load(open('passes.pkl', 'rb'))
    camera = SatelliteTracker()

    #import pdb; pdb.set_trace()
    print("Calibrate position")

    do_jog = input("Need to jog? (y/n): ")
    if do_jog == 'y':
        jog()
    elif do_jog == 'n':
        pass
    else:
        print("Invlid input")
        exit(1)

    ra = float(input("Please enter current RA: "))
    dec = float(input("Please enter current dec: "))

    if not mock:
        camera.mount_init()
        camera.calibrate(ra, dec)
        
    run_observations(camera, passes, ts, mock)


if __name__ == '__main__':
    main()
