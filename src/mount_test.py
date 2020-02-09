import mount as mt
import pytest
import time


def test_position():
    m = mt.GoToMount()
    a = m.position
    print(a)


def test_get_steps_per_deg():
    m = mt.GoToMount()
    a = m.steps_per_deg
    print(a)


def test_move():
    m = mt.GoToMount()
    m.move_relative(val=20, axis=m.RA_CHANNEL, use_degrees=True)
    assert m.is_moving
    m.stop(m.RA_CHANNEL)
    time.sleep(.1) 
    assert not m.is_moving


def test_get_stats():
    m = mt.GoToMount()
    print(m.is_moving)


@pytest.mark.skip(reason="only when debugging position")
def test_position_change():
    m = mt.GoToMount()
    m.move(0, 1)
    m._stream_position(10)
    m.stop(1)


def test_value_decode():
    m = mt.GoToMount()

    out = 8120368
    inp = b'30E87B'

    b_d = m._decode(inp)
    assert b_d == out


def test_value_encode():
    m = mt.GoToMount()
    inp = 8120368
    out = '30E87B'

    a_d = m._encode(inp)
    assert a_d == out


def test_target_setting():
    m = mt.GoToMount()
    target = 41276
    m._set_move_target(target=target, axis=m.RA_CHANNEL)
    ra, dec = m.target
    assert target == ra 


def test_relative_movement():
    m = mt.GoToMount()
    target = 10  # degrees
    m.move_relative(val=target, axis=m.DEC_CHANNEL, use_degrees=True)
    while m.is_moving:
        time.sleep(.1)
    m.move_relative(val=-target, axis=m.DEC_CHANNEL, use_degrees=True)

