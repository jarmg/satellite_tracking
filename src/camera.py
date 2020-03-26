from mount import GoToMount
import time
import logging
import os
import subprocess

from skyfield.api import load
ts = load.timescale()


hostname = "ESP_6DAE10"
serial_port = 11880


class SatelliteTracker:
    def __init__(self):
        self.root_dir = os.environ['ROOT_DIR']
        self.util_dir = os.path.join(self.root_dir + 'utils')
        self.mount = None
        self._zero_ra_pos = None
        self._zero_dec_pos = None
        self._ra_steps_per_deg = None
        self._dec_steps_per_deg = None

    def mount_init(self, ip=hostname, port=serial_port):
        self.mount = GoToMount(ip_address=ip, port=port)
        self._ra_steps_per_deg, self._dec_steps_per_deg = \
            self.mount.steps_per_deg

    def _ra_to_steps(self, ra):
        return int(self._zero_ra_pos + (ra * self._ra_steps_per_deg))

    def _dec_to_steps(self, dec):
        return int(self._zero_dec_pos + (dec * self._dec_steps_per_deg))

    @property
    def ra(self):
        ra_step_pos, _ = self.mount.position
        return (ra_step_pos - self._zero_ra_pos)/self._ra_steps_per_deg

    @property
    def dec(self):
        dec_step_pos, _ = self.mount.position
        return (dec_step_pos - self._zero_dec_pos)/self._dec_steps_per_deg

    def calibrate(self, ra, dec):
        '''Given a known RA and DEC, set a baseline position'''
        ra_pos, dec_pos = self.mount.position
        self._zero_ra_pos = ra_pos - (self.mount.steps_per_deg[0] * ra)
        self._zero_dec_pos = dec_pos - (self.mount.steps_per_deg[1] * dec)

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
            self.mount.move_relative(val=ra, axis=self.mount.RA_CHANNEL)
        if dec:
            self.mount.move_relative(val=dec, axis=self.mount.DEC_CHANNEL)

    def take_pictures(self, file_path, exposure, count):
        print("capturing image")
        ret = subprocess.run([
            os.join(self.util_dir, "capture_images.sh"),
            str(count),
            str(exposure),
            file_path
        ])
        print("return of {}".format(ret))

    def move_to_then_shoot(self, ra, dec, t, margin, exposure, output_dir):
        '''
            time: expected time of event (gps)
            margin: buffer before and after event to image to increase our odds
            exposure: length of the exposure
        '''
        self.move_to(ra, dec)

        # build the observation window (interesting:https://bit.ly/2Wz5YwC)
        mg_dt = margin / 24 / 60 / 60
        expsr = margin / 24 / 60 / 60

        begin = ts.tt_jd(t.tt - mg_dt)
        end = ts.tt_jd(t.tt + mg_dt)
        imgs = int((end.tt - begin.tt) / expsr)
        while begin.tt > ts.now().tt:
            print("starting exposure of {ra}, {dec} in T-{t_minus} seconds at time {tt}".format(
                ra=ra, dec=dec, t_minus=((begin.tt - ts.now().tt)) * 60 * 60 * 24), begin.tt)
            time.sleep(1)
        self.take_pictures(output_dir, exposure, imgs)
        print("done taking images")







        

        



