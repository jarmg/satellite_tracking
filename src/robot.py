import threading

from camera import SatelliteTracker
from utils import run_jog_loop
from session_runner import Session


# Set your home location

# check for status of stuff

# set up a new session

class Robot:
    '''instance of a booted system. Should hold state between runs'''

    def __init__(self):
        self.tracker = SatelliteTracker()
        self.tracker.mount_init()
        self.session = Session()
        self._session_thread = None
        self._stop_event = None

    def reset_session(self):
        self._current_session = Session()

    def terminal_calibration(self):
        print("Calibrate position")
        do_jog = input("Need to jog? (y/n): ")
        if do_jog == 'y':
            run_jog_loop(self.tracker)
        elif do_jog == 'n':
            pass
        else:
            print("Invalid input")
            exit(1)

        az = float(input("Please enter current azimuth: "))
        el = float(input("Please enter current elevation: "))
        self.calibrate(az, el)

    def calibrate(self, az, el):
        self.tracker.calibrate(az=az, el=el)

    def start_session(self):
        if not self.tracker.is_calibrated:
            raise(RuntimeError(
                "Must calibrate before running oberservations"))
        self._stop_event = threading.Event()
        self._session_thread = \
            threading.Thread(
                target=self.session.run_observations,
                name='observation_session',
                args=(self.tracker, self._stop_event))
        self._session_thread.start()

    def stop_session(self):
        if self._session_thread is None:
            raise(RuntimeError("No session in progress"))
        self._stop_event.set()
