from skyfield.api import Topos, load, Loader
import pickle

time_loader = Loader('./data/')

def get_satellites(tle_file=None):
    if tle_file:
        satellites = load.tle(tle_file)

    else:
        celestrak_url = 'https://celestrak.com/NORAD/elements/starlink.txt' 
        satellites = load.tle(celestrak_url)

    starlinks = {k: v for k, v in satellites.items() if 'STARLINK' in str(k)}
    return starlinks


def _get_passes_for_sat(satellite, location, t0, t1):
    event_times, events = satellite.find_events(location, t0, t1, altitude_degrees=30.0)
    diff = satellite - location

    # 1 == pass culminated
    peaks = [event_times[i] for i in range(len(event_times)) if events[i] == 1]

    ret = [(satellite.name, p, diff.at(p).altaz()) for p in peaks]
    return ret 

def exmaple_at():
    sats = get_satellites()
    s1 = list(sats.values())[0]
    ts = time_loader.timescale(builtin=True)
    t0 = ts.utc(2019, 2, 22)
    return s1.at(t0)

def get_upcoming_passes(location, t0, t1, tle_file=None, cache=False):
    sats = get_satellites(tle_file)
    passes = []
    for sat in list(sats.values()):
        passes += _get_passes_for_sat(sat, location, t0, t1)

    if cache:
        pickle.dump(passes, open("passes.pkl", 'wb'))

    return passes

def main():
    ts = time_loader.timescale(builtin=True)
    location = Topos('47.647654 N', '-122.324748 W')
    t0 = ts.utc(2020, 2, 22)
    t1 = ts.utc(2020, 2, 25)

    return get_upcoming_passes(location, t0, t1, cache=True, tle_file='starlink.txt')

    #sats = get_satellites()
    #passes = _get_passes_for_sat(list(sats.values())[0], location, t0, t1)
    #return passes


if __name__ == "__main__":
    (main())
