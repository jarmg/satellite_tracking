import socket
import logging
import time

logging.basicConfig(level=logging.INFO)

# Motorcontroller: https://indilib.org/media/kunena/attachments/4026/SkywatcherMotorControllerCommandSet.pdf


class GoToMount:

    RA_CHANNEL = 1
    DEC_CHANNEL = 2
    RA_AND_DEC = 3
    FAST_GOTO = 0
    COARSE_GOTO = 4

    CMDS = {

        # motor controller communication
        'get_steps_per_rev': ':a{axis}\r',
        'get_position': ':j{axis}\r',
        'get_status': ':f{axis}\r',
        'get_goto_target': ':h{axis}\r',
        'emergency_stop': ':L{axis}\r',
        'start_motion': ':J{axis}\r',
        'stop_motion': ':K{axis}\r',
        'set_motion_mode': ':G{axis}{motion_type}{motion_orientation}\r',
        'set_goto_target': ':S{axis}{target}\r',
        'aux_on': ':O1{axis}\r',
        'aux_off': 'O0{axis}\r',

        # networking commands (all had to be packet sniffed)
        'set_wifi': 'AT+CWJAP_DEF="{ssid}","{pwd}"\r\n',
        'get_dhcp_info': 'AT+CWDHCP_DEF?\r\n',
        'get_network_mode': 'AT+CWMODE_CUR?\r\n',
        'get_network_info': 'AT+CIPSTA_CUR?\r\n',
        'get_ap_info': 'AT+CWSAP_CUR?\r\n',
        'get_wifi_info': 'AT+CWJAP_DEF?\r\n'
    }

    # TODO: May need to lock this if we see issues between client requests
    def __init__(self, ip_address="ESP_6DAE10", port=11880):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._ip_address = ip_address
        self._port = port
        self._socket.settimeout(4)

    def _send(self, msg):
        logging.debug("sending msg'{}".format(repr(msg)))
        self._socket.sendto(
            bytes(msg, encoding='ascii'), (self._ip_address, self._port))

    def _send_and_rcv(self, msg, is_motor_msg):
        self._send(msg)
        return self._socket.recvfrom(1024)[0]

    def _send_and_rcv_with_retry(self, msg, is_motor_msg=True):
        retry = True
        retry_count = 0
        retry_max = 20
        while(retry):
            try:
                ret = self._send_and_rcv(msg, is_motor_msg)
                retry = False
            except socket.timeout:
                print("retry # {}".format(retry_count))
                retry_count += 1
                if retry_count < retry_max:
                    retry = True
                else:
                    raise socket.timeout

        if b"!" in ret:
            raise ValueError('Motor controller error: {}'.format(ret))
        if is_motor_msg:
            return ret[1:-1]  # strip '=' and '\r'
        return ret

    def _stream_position(self, seconds):
        start = time.time()
        while (time.time() < start + seconds):
            ra = self._send_and_rcv_with_retry(
                self.CMDS['get_position'].format(axis=self.RA_CHANNEL))
            val = self._decode(ra, is_position=True)
            print("raw: {ra}, decoded: {val}".format(ra=ra, val=val))

    def _encode(self, val, is_position=False):
        '0xABCDEF -> 0xEFCDAB'
        # Build byte array

        # position values have an offset of 0x800000
        if is_position:
            val += 0x800000

        hx = val.to_bytes(3, byteorder='big').hex().upper()

        # Reorder bytes
        order = [4, 5, 2, 3, 0, 1]
        bv = [hx[i] for i in order]
        return ''.join(bv)

    def _decode(self, val, is_position=False):
        '0xEFCDAB -> 0xABCDEF '
        # Get hex string
        v = val.decode()

        # Reorder
        order = [4, 5, 2, 3, 0, 1]
        b = [v[i] for i in order]

        # Convert back to int
        h = int(''.join(b), base=16)

        # apply offset if position
        if is_position:
            return h - 0x800000

        return h

    @property
    def target(self):
        ra = self._decode(self._send_and_rcv_with_retry(
            self.CMDS['get_goto_target'].format(axis=self.RA_CHANNEL)),
            is_position=True
        )
        dec = self._decode(self._send_and_rcv_with_retry(
            self.CMDS['get_goto_target'].format(axis=self.DEC_CHANNEL)),
            is_position=True
        )
        return(ra, dec)

    @property
    def position(self):
        ra = self._send_and_rcv_with_retry(
            self.CMDS['get_position'].format(axis=self.RA_CHANNEL))
        print("GOT POSITION {}".format(ra))
        dec = self._send_and_rcv_with_retry(
            self.CMDS['get_position'].format(axis=self.DEC_CHANNEL))
        print("GOT POSITION {}".format(dec))
        ra_value = self._decode(ra, is_position=True)
        dec_value = self._decode(dec, is_position=True)
        return(ra_value, dec_value)

    @property
    def is_moving(self):
        ra = self._send_and_rcv_with_retry(
            self.CMDS['get_status'].format(axis=self.RA_CHANNEL))
        dec = self._send_and_rcv_with_retry(
            self.CMDS['get_status'].format(axis=self.DEC_CHANNEL))
        ra_running = ra[1] % 2
        dec_running = dec[1] % 2
        return bool(ra_running + dec_running)

    @property
    def steps_per_deg(self, decimal=True):
        ra = self._decode(self._send_and_rcv_with_retry(
            self.CMDS['get_steps_per_rev'].format(axis=self.RA_CHANNEL)))
        dec = self._decode(self._send_and_rcv_with_retry(
            self.CMDS['get_steps_per_rev'].format(axis=self.DEC_CHANNEL)))
        return(ra/360.0, dec/360.0)

    def set_wifi(self, ssid, password, timeout=20):
        msg = self.CMDS['set_wifi'].format(ssid=ssid, pwd=password)
        self._send(msg) # no ack for set wifi

        # send until we lose connection
        end = time.time() + timeout
        while(time.time() < end):
            try:
                self._send_and_rcv(
                    self.CMDS['get_status'].format(axis=self.RA_CHANNEL), is_motor_msg=True)
                self._send(msg)
            except socket.timeout:
                return


        
    def get_wifi(self) -> (str, str):
        '''example return:
            b'+CWJAP_DEF:"CenturyLink6635","70:f2:20:61:9e:a3",11,-72\r\n\r\nOK\r\n'
        '''
        msg = self.CMDS['get_wifi_info']
        ret = self._send_and_rcv_with_retry(msg, is_motor_msg=False) # Note: no receive because wifi setting doesn't return an ack
        try:
            ssid, mac, channel, _ = str(ret).split(',')
            ssid = ssid.split('CWJAP_DEF:')[1] 
        except IndexError:
            raise ValueError("Invalid wifi response format: {}".format(ret))


        # strip quotation marks and return
        return ssid[1:-1], mac[1:-1] 
        

    def _set_motion(self, mode, orientation, axis):
        cmd = self.CMDS['set_motion_mode'].format(
            axis=axis,
            motion_type=mode,
            motion_orientation=orientation
        )
        self._send_and_rcv_with_retry(cmd)

    def _set_move_target(self, target, axis):
        val = self._encode(target, is_position=True)
        cmd = self.CMDS['set_goto_target'].format(axis=axis, target=val)
        self._send_and_rcv_with_retry(cmd)

    def stop(self, axis):
        cmd = self.CMDS['stop_motion'].format(axis=axis)
        self._send_and_rcv_with_retry(cmd)

    def move(self, val, axis):
        self._set_motion(self.FAST_GOTO, self.COARSE_GOTO, axis)
        self._set_move_target(val, axis)
        self._send_and_rcv_with_retry(
            self.CMDS['start_motion'].format(axis=axis))

    def move_relative(self, value, axis, use_degrees=True):
        logging.debug(
            "relative movement value:{}, axis:{}".format(value, axis))
        delta = value
        ax_idx = axis - 1
        if use_degrees:
            steps_per_deg = self.steps_per_deg[ax_idx]
            delta = steps_per_deg * value

        logging.debug("delta value:{}".format(delta))
        logging.debug("steps per deg:{}".format(self.steps_per_deg))
        pos = self.position[ax_idx]
        pos += delta
        self.move(int(pos), axis=axis)

    # Not used (couldn't get this to work)
    def shutter_on(self, axis):
        self._send_and_rcv_with_retry(self.CMDS['aux_on'].format(axis=axis))

    # Not used (couldn't get this to work)
    def shutter_off(self, axis):
        self._send_and_rcv_with_retry(self.CMDS['aux_off'].format(axis=axis))
