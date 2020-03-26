import os
import pickle

from skyfield.api import Topos, load, Loader

time_loader = Loader('./data/')
ROOT_DIR = os.environ['ROOT_DIR']


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


def main():
    ts = time_loader.timescale(builtin=True)
    location = Topos('47.647654 N', '-122.324748 W')
    t0 = ts.now()
    end = list(t0.utc)
    end[2] += 2  # forecast 2 days forward
    t1 = ts.utc(*end)

    return get_upcoming_passes(location, t0, t1, cache=True, tle_file=None)


if __name__ == "__main__":
    (main())
