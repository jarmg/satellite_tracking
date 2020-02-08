import socket
import logging
import time

logging.basicConfig(level=logging.INFO)

# Motorcontroller: https://indilib.org/media/kunena/attachments/4026/SkywatcherMotorControllerCommandSet.pdf

ip_address = "192.168.0.17"
serial_port = 11880

class GoToMount:

    RA_CHANNEL = 1
    DEC_CHANNEL = 2
    FAST_GOTO = 0
    COARSE_GOTO = 4

    CMDS = {
        'get_steps_per_rev': ':a{axis}\r',
        'get_position': ':j{axis}\r',
        'get_status': ':f{axis}\r',
        'get_goto_target': ':h{axis}\r',
        'emergency_stop': ':L{axis}\r',
        'start_motion': ':J{axis}\r',
        'stop_motion': ':K{axis}\r',
        'set_motion_mode': ':G{axis}{motion_type}{motion_orientation}\r',
        'set_goto_target': ':S{axis}{target}\r'
    }

    def __init__(self, ip_address="192.168.0.17", port=11880):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._ip_address = ip_address
        self._port = port
        self._socket.settimeout(5)
        self._ra = None
        self._dec = None

    def _send_and_receive(self, msg):
        logging.debug("sending msg'{}".format(repr(msg)))
        self._socket.sendto(bytes(msg, encoding='ascii'), (ip_address, serial_port))
        ret = self._socket.recvfrom(1024)[0]
        if b"!" in ret:
            raise ValueError('Motor controller error: {}'.format(ret))
        return ret[1:-1]  # strip '=' and '\r'

    def _stream_position(self, seconds):
        import time
        start = time.time()
        while (time.time() < start + seconds):
            ra = self._send_and_receive(
                    self.CMDS['get_position'].format(axis=self.RA_CHANNEL))
            val = self._decode(ra)
            print("raw: {ra}, decoded: {val}".format(ra=ra, val=val))

    def _encode(self, val):
        '0xABCDEF -> 0xEFCDAB'
        # Build byte array
        hx = val.to_bytes(3, byteorder='big').hex().upper()

        # Reorder bytes
        order = [4, 5, 2, 3, 0, 1] 
        bv = [hx[i] for i in order]
        return ''.join(bv)

    def _decode(self, val):
        '0xEFCDAB -> 0xABCDEF '
        # Get hex string
        v = val.decode()

        # Reorder
        order = [4, 5, 2, 3, 0, 1] 
        b = [v[i] for i in order]

        # Convert back to int
        h = int(''.join(b), base=16)

        return h 

    @property
    def target(self):
        ra = self._decode(self._send_and_receive(
                self.CMDS['get_goto_target'].format(axis=self.RA_CHANNEL)))
        dec = self._decode(self._send_and_receive(
                self.CMDS['get_goto_target'].format(axis=self.DEC_CHANNEL)))
        return(ra, dec)

    @property
    def position(self):
        ra = self._send_and_receive(
                self.CMDS['get_position'].format(axis=self.RA_CHANNEL))
        dec = self._send_and_receive(
                self.CMDS['get_position'].format(axis=self.DEC_CHANNEL))
        ra_value = self._decode(ra)
        dec_value = self._decode(dec)
        return(ra_value, dec_value)

    @property
    def is_moving(self):
        ra = self._send_and_receive(
                self.CMDS['get_status'].format(axis=self.RA_CHANNEL))
        dec = self._send_and_receive(
                self.CMDS['get_status'].format(axis=self.DEC_CHANNEL))
        ra_running = ra[1] % 2
        dec_running = dec[1] % 2
        return bool(ra_running + dec_running)

    @property
    def steps_per_rev(self, decimal=True):
        ra = self._decode(self._send_and_receive(
                self.CMDS['get_steps_per_rev'].format(axis=self.RA_CHANNEL)))
        dec = self._decode(self._send_and_receive(
                self.CMDS['get_steps_per_rev'].format(axis=self.DEC_CHANNEL)))
        return(ra, dec)

    def _set_motion(self, mode, orientation, axis): 
        cmd = self.CMDS['set_motion_mode'].format(
            axis=axis,
            motion_type=mode,
            motion_orientation=orientation
        )
        self._send_and_receive(cmd)

    def _set_move_target(self, target, axis):
        val = self._encode(target)
        cmd = self.CMDS['set_goto_target'].format(axis=axis, target=val)
        self._send_and_receive(cmd)

    def stop(self, axis):
        cmd = self.CMDS['stop_motion'].format(axis=axis)
        self._send_and_receive(cmd)

    def move(self, target, axis):
        self._set_motion(self.FAST_GOTO, self.COARSE_GOTO, axis)
        self._set_move_target(target, axis)
        self._send_and_receive(self.CMDS['start_motion'].format(axis=axis))
        
    def move_relative(self, val, axis, use_degrees=True):
        delta = val
        ax_idx = axis - 1
        if use_degrees:
            steps_per_deg = self.steps_per_rev[ax_idx] / 360
            delta = steps_per_deg * val 
        curr_pos = self.position[ax_idx]
        new_pos = int(curr_pos + delta)
        self.move(new_pos, axis)
        










