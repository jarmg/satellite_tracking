from mount import GoToMount
import time
import logging
import os
import subprocess

ip_address = "192.168.0.17"
serial_port = 11880


class SatelliteTracker:
    def __init__(self):
        self.mount = None
        self._zero_ra_pos = None
        self._zero_dec_pos = None
        self._ra_steps_per_deg = None
        self._dec_steps_per_deg = None

    def mount_init(self, ip=ip_address, port=serial_port):
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

    def move_to(self, ra, dec):
        '''blocks on movement'''
        ra = self._ra_to_steps(ra)
        dec = self._dec_to_steps(dec)
        self.wait_for_move()
        self.mount.move(ra, axis=self.mount.RA_CHANNEL)
        self.wait_for_move()
        self.mount.move(dec, axis=self.mount.DEC_CHANNEL)
        self.wait_for_move()

    def wait_for_move(self):
        while self.mount.is_moving:
            time.sleep(.1)
        return

    def move_relative(self, ra=None, dec=None):
        if ra:
            self.mount.move_relative(val=ra, axis=self.mount.RA_CHANNEL)
        if dec:
            self.mount.move_relative(val=dec, axis=self.mount.DEC_CHANNEL)

    def take_pictures(self, file_path, exposure, count):
        print("capturing image")
        ret = subprocess.run([
            "./capture_images.sh",
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
        begin = t - margin
        end = t + margin
        imgs = (end - begin) / exposure
        while begin > time.time():
            print("starting exposure of {ra}, {dec} in T-{t_minus} seconds".format(
                ra=ra, dec=dec, t_minus=(begin - time.time())))
            time.sleep(1)
        self.take_pictures(output_dir, exposure, imgs)
        print("done taking images")







        

        



