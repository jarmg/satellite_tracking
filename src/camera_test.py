import camera as c
import pytest

@pytest.mark.skip(reason="Can't run at the same time")
def test_relative_move():
    s = c.SatelliteTracker()
    s.move_relative(ra=10)

def test_calibration():
    s = c.SatelliteTracker()
    s.calibrate(ra=00, dec=0)
    print(s.ra)
    print(s.dec)
    s.move_to(ra=45, dec=45)
    s.move_to(ra=0, dec=0)

