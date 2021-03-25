#
# os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4
# os.environ["OPENBLAS_NUM_THREADS"] = "1"  # export OPENBLAS_NUM_THREADS=4
# os.environ["MKL_NUM_THREADS"] = "1"  # export MKL_NUM_THREADS=6
# os.environ["VECLIB_MAXIMUM_THREADS"] = "1"  # export VECLIB_MAXIMUM_THREADS=4
# os.environ["NUMEXPR_NUM_THREADS"] = "1"  # export NUMEXPR_NUM_THREADS=6

import cProfile
import time

import numpy as np

import pstats

def foo(nums=50):
    s = 0
    is_numpy = True
    if is_numpy:
        Xrow = np.ones((100, 20))
        X = np.ones((600, 20))
        for i in range(nums):
            s = np.matmul(X, Xrow.T)

        # del Xrow, X
    else:
        s = 0
        for i in range(10000000):
            s += i


def process_timing(name=''):
    pr = cProfile.Profile(time.process_time)
    pr.enable()

    foo()
    # time.sleep(1)

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative

    return ps.total_tt


def perf_counter_timing(name=''):
    pr = cProfile.Profile(time.perf_counter)
    pr.enable()

    foo()
    # time.sleep(1)

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative

    return ps.total_tt


n_repeats = 10
res = []
for i in range(n_repeats):
    res.append(process_timing())
print(f'process_time: {np.mean(res):.5f}+/-{np.std(res):.5f}')

for i in range(n_repeats):
    res.append(perf_counter_timing())
print(f'perf_counter: {np.mean(res):.5f}+/-{np.std(res):.5f}')
