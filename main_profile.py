"""

"""
import numpy as np
from parallel import parallel_func
from serial import serial_func
import cProfile

def main(is_numpy=False):
    """ Get the time taken on foo() function measured by time.time() and time.process_time()
    """
    n_repeats = 10

    print('\nserial')
    pr=cProfile.Profile()
    pr.enable()
    res = serial_func(n_repeats, is_numpy)
    pr.disable()
    pr.print_stats()
    for name_, vs_ in res:
        print(f'{name_:20}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}', [f'{v:.5f}' for v in vs_])

    print('\nparallel')
    pr = cProfile.Profile()
    pr.enable()
    res = parallel_func(n_repeats, n_jobs=2, is_numpy=is_numpy)
    pr.disable()
    pr.print_stats()
    for (name_, vs_) in res:
        print(f'{name_:20}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}', [f'{v:.5f}' for v in vs_])


if __name__ == '__main__':
    print('===========================================================================')
    print('1 ***use numpy array')
    main(is_numpy=True)

    print('\n===========================================================================')
    print('2 ***don\'t use numpy array')
    main(is_numpy=False)
