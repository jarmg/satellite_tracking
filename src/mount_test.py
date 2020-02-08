import mount_control as tc
import pytest
import time

def test_move():
    m = tc.GoToMount() 
    
def test_position():
    m = tc.GoToMount()
    a = m.position
    print(a)

def test_get_steps_per_rev():
    m = tc.GoToMount()
    a = m.steps_per_rev
    print(a)

def test_move():
    m = tc.GoToMount()
    a = m.steps_per_rev
    m.move(int(a[0]/2), 1)
    assert m.is_moving
    m.stop(1)
    time.sleep(.1) 
    assert not m.is_moving

    print(a)

def test_get_stats():
    m = tc.GoToMount()
    print(m.is_moving)

@pytest.mark.skip(reason="only when debugging position")
def test_position_change():
    m = tc.GoToMount()
    m.move(0, 1)
    m._stream_position(10)
    m.stop(1)


def test_value_decode():
    m = tc.GoToMount()

    out = 8120368
    inp = b'30E87B'

    b_d = m._decode(inp)
    assert b_d == out


def test_value_encode():
    m = tc.GoToMount()
    inp = 8120368
    out = '30E87B'

    a_d = m._encode(inp)
    assert a_d == out


def test_target_setting():
    m = tc.GoToMount()
    target = 41276
    m._set_move_target(target=target, axis=m.RA_CHANNEL)
    ra, dec = m.target
    assert target == ra 


def test_relative_movement():
    m = tc.GoToMount()
    target = 20 #degrees
    m.move_relative(val=target, axis=m.DEC_CHANNEL, use_degrees=True)

