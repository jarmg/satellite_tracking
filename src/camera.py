from mount import GoToMount
import time

ip_address = "192.168.0.17"
serial_port = 11880


class SatelliteTracker:
    def __init__(self):
        self.mount = GoToMount(ip_address=ip_address, port=serial_port)
        self._zero_ra_pos = None
        self._zero_dec_pos = None
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

    def wait_for_move(self):
        while self.mount.is_moving:
            time.sleep(.1)
        return

    def move_relative(self, ra=None, dec=None):
        if ra:
            self.mount.move_relative(val=ra, axis=self.mount.RA_CHANNEL)
        if dec:
            self.mount.move_relative(val=dec, axis=self.mount.DEC_CHANNEL)
