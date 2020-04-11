import camera as c
import pytest
import time
import subprocess


@pytest.mark.skip(reason="Can't run at the same time")
def test_relative_move():
    s = c.SatelliteTracker()
    s.move_relative(ra=10)


@pytest.mark.skip(reason="Can't run at the same time")
def test_calibration():
    s = c.SatelliteTracker()
    s.calibrate(ra=00, dec=0)
    print(s.ra)
    print(s.dec)
    s.move_to(ra=45, dec=45)
    s.move_to(ra=0, dec=0)

'''
def test_shutter():
    s = c.SatelliteTracker()
    s.mount.shutter_on(2)
    time.sleep(1)
    s.mount.shutter_off(2)
'''

def test_take_picture():
    s = c.SatelliteTracker()
    s.take_picture(file_path="test_outputs", exposure_time=1)

def test_subprocess():
    p = subprocess.run(['./capture_images.sh', '1', '1',  'testing_outs'])
