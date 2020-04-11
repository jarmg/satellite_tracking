import time
import logging
import os
import subprocess

from mount import GoToMount
from predict_passes import get_moon_pos


#hostname = "ESP_6DAE10.home"
hostname = "192.168.0.17"
serial_port = 11880


class SatelliteTracker:
    def __init__(self):
        self.root_dir = os.environ['ROOT_DIR']
        self.util_dir = os.path.join(self.root_dir, 'utils')
        self.mount = None
        self._zero_az_pos = None
        self._zero_el_pos = None
        self._ra_steps_per_deg = None
        self._dec_steps_per_deg = None
        self.is_calibrated = False

    def requires_calibration(func):
        def check_calibration(*args, **kwargs):
            print("move_calib")
            self = args[0]
            if self.is_calibrated:
                func(args, kwargs)
            else:
                raise ValueError("Camera is not calibrate")

    def mount_init(self, ip=hostname, port=serial_port):
        self.mount = GoToMount(ip_address=ip, port=port)
        self._ra_steps_per_deg, self._dec_steps_per_deg = \
            self.mount.steps_per_deg

    def _ra_to_steps(self, ra):
        return int(self._zero_az_pos + (ra * self._ra_steps_per_deg))

    def _dec_to_steps(self, dec):
        return int(self._zero_el_pos + (dec * self._dec_steps_per_deg))

    @property
    def az(self):
        ra_step_pos, _ = self.mount.position
        return (ra_step_pos - self._zero_az_pos)/self._ra_steps_per_deg

    @property
    def el(self):
        _, el_step_pos = self.mount.position
        return (el_step_pos - self._zero_el_pos)/self._dec_steps_per_deg

    def calibrate(self, az, el):
        '''Given a known RA and DEC, set a baseline position'''
        az_pos, el_pos = self.mount.position
        self._zero_az_pos = az_pos - (self.mount.steps_per_deg[0] * az)
        self._zero_el_pos = el_pos - (self.mount.steps_per_deg[1] * el)
        self.is_calibrated = True

    def wait_for_move(self):
        while self.mount.is_moving:
            time.sleep(.1)
        return

    def move_to(self, ra, dec):
        '''blocks on movement'''
        ra = self._ra_to_steps(ra)
        dec = self._dec_to_steps(dec)
        self.wait_for_move()
        self.mount.move(ra, axis=self.mount.RA_CHANNEL)
        self.wait_for_move()
        self.mount.move(dec, axis=self.mount.DEC_CHANNEL)
        self.wait_for_move()

    def move_relative(self, ra=None, dec=None):
        if ra:
            self.mount.move_relative(value=ra, axis=self.mount.RA_CHANNEL)
        if dec:
            self.mount.move_relative(value=dec, axis=self.mount.DEC_CHANNEL)

    def take_pictures(self, file_path, file_name, exposure, count):
        print("capturing image")
        ret = subprocess.run([
            os.path.join(self.util_dir, "capture_images.sh"),
            str(count),
            str(exposure),
            file_path,
            file_name
        ])
        print("return of {}".format(ret))
        return file_path
