import pickle

from skyfield.api import Loader

load = Loader('./data/')

def main():
    ts = load.timescale(builtin=True)

    current = ts.now()

    # load, sort, and filter sat passes
    passes = pickle.load(open('passes.pkl', 'rb'))
    sp = sorted(passes, key=lambda p: p[1].tt)
    sp = list(filter(lambda a: a[1].tt > current.tt, sp))


    return sp


if __name__ == '__main__':
    print(main())


    



