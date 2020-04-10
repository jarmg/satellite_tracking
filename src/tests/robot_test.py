import time

from robot import Robot


def test_calibration():
    r = Robot()
    r.calibrate(13, 20)
    assert(r.tracker.az == 13)
    assert(r.tracker.el == 20)
    assert(r.tracker.is_calibrated)    


def test_run():
    r = Robot()
    r.calibrate(13, 20)
    assert(r.tracker.az == 13)
    assert(r.tracker.el == 20)
    assert(r.tracker.is_calibrated)    

    r.start_session()

    time.sleep(10)

    r.stop_session()

