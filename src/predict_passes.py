import os
import sys
import pickle

from skyfield.api import Topos, load, Loader

ROOT_DIR = os.environ['ROOT_DIR']

time_loader = Loader('./data/')
ts = time_loader.timescale(builtin=True)
planets = load('de421.bsp')

def get_moon_pos():
    earth = planets['earth']
    moon = planets['moon']

    # Jared's home
    loc = earth + Topos('47.647654 N', '-122.324748 E')
    apparent = loc.at(ts.now()).observe(moon).apparent()
    return apparent.altaz()



def get_satellites(tle_file=None):
    if tle_file:
        satellites = load.tle(tle_file)

    else:
        celestrak_url = 'https://celestrak.com/NORAD/elements/starlink.txt' 
        satellites = load.tle(celestrak_url)

    starlinks = {k: v for k, v in satellites.items() if 'STARLINK' in str(k)}
    return starlinks


def _get_passes_for_sat(satellite, location, t0, t1):
    event_times, events = satellite.find_events(
            location, t0, t1, altitude_degrees=30.0)
    diff = satellite - location

    # 1 == pass culminated
    peaks = [event_times[i] for i in range(len(event_times)) if events[i] == 1]

    ret = [(satellite.name, p, diff.at(p).altaz()) for p in peaks]
    return ret


def get_upcoming_passes(location, t0, t1, tle_file=None, cache=False):
    sats = get_satellites(tle_file)
    passes = []
    for sat in list(sats.values()):
        passes += _get_passes_for_sat(sat, location, t0, t1)

    if cache:
        data_dir = os.path.join(ROOT_DIR, 'data', 'passes.pkl')
        pickle.dump(passes, open(data_dir, 'wb'))

    return passes


def predict_passes(lat, lon):
    # get observer location
    location = Topos(lat + ' N', lon + 'W')

    # build time range for predictions
    t0 = ts.now()
    end = list(t0.utc)
    end[2] += 2  # forecast 2 days forward
    t1 = ts.utc(*end)

    return get_upcoming_passes(location, t0, t1, cache=True, tle_file=None)


if __name__ == "__main__":
    lat = sys.argv[1]
    lon = sys.argv[2]
    if lat in None or lon is None:
        raise ValueError("Invlaid lat lon!")
    predict_passes()
