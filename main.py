
import numpy as np
from parallel import parallel_func
from serial import serial_func


def main():
    n_repeats = 10

    print('\nserial')
    res = serial_func(n_repeats)
    for name_, vs_ in res:
        print(f'{name_:20}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}', [f'{v:.5f}' for v in vs_])

    print('\nparallel')
    res = parallel_func(n_repeats, n_jobs=2)
    for (name_, vs_) in res:
        print(f'{name_:20}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}', [f'{v:.5f}' for v in vs_])


if __name__ == '__main__':
    main()
