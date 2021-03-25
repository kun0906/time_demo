import os

os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4
os.environ["OPENBLAS_NUM_THREADS"] = "1"  # export OPENBLAS_NUM_THREADS=4
os.environ["MKL_NUM_THREADS"] = "1"  # export MKL_NUM_THREADS=6
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"  # export VECLIB_MAXIMUM_THREADS=4
os.environ["NUMEXPR_NUM_THREADS"] = "1"  # export NUMEXPR_NUM_THREADS=6

import cProfile
import os
import time
from func_timeout import func_set_timeout

import pstats

from joblib import Parallel, delayed
import numpy as np
print(np.__config__.show())
# from joblib import Parallel, delayed    # implicitly use max threads
FUNC_TIMEOUT = 3 * 60

from pickle import dump, load


# @func_set_timeout(FUNC_TIMEOUT)  # seconds
def foo():
    s = 0
    is_numpy = True
    if is_numpy:
        Xrow = np.ones((100, 20))
        X = np.ones((600, 20))
        for i in range(20):
            s = np.matmul(X, Xrow.T)

        del Xrow, X
    else:
        s = 0
        for i in range(10000000):
            s += i


# @func_set_timeout(FUNC_TIMEOUT)  # seconds
def timing(name=''):
    # print('timing')
    # start = time.time()
    # pr = cProfile.Profile(time.time)
    # pr.enable()
    s=0
    is_numpy = True
    if is_numpy:
        Xrow = np.ones((100, 20))
        X = np.ones((600, 20))
        for i in range(20):
            s = np.matmul(X, Xrow.T)

        del Xrow, X
    else:
        s = 0
        for i in range(10000000):
            s += i

    # pr.disable()
    # ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    # ps.print_stats()
    # del ps
    # end = time.time()
    # print('timing:', end-start)
    return s


def timing2(name=''):
    # start = time.process_time()
    pr = cProfile.Profile(time.time)
    pr.enable()

    foo()
    # time.sleep(1)

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    # end = time.process_time()
    # print(end-start)

    # # time.sleep(1)
    # for i in range(5):
    #     foo()

    start = time.process_time()
    pr = cProfile.Profile(time.time)
    pr.enable()

    timing()

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    # ps.print_stats()
    # print(f'{ps.total_tt}')

    return ps.total_tt
    # end = time.process_time()
    # # del timing
    # return end - start

print('**serail')
n_repeats = 200
res = []
for i in range(n_repeats):
    res.append(timing2())
print(f'{np.mean(res):.5f}+/-{np.std(res):.5f}')

print('**parallel')
# pre_dispatch='2 * n_jobs', batch_size='auto', temp_folder=None
with Parallel(n_jobs=3, verbose=0, backend='loky') as parallel:
    res = parallel(delayed(timing2)(name_) for name_ in range(n_repeats))
print(f'{np.mean(res):.5f}+/-{np.std(res):.5f}, ')

# timing()
# timing2()


# #
# #
# # # from pprint import pprint
# #
# # import pstats
# import time
# # from function import foo
# # import cProfile
# # #
# # # is_numpy = True
# # # # cProfile.run(f'foo(is_numpy={is_numpy})')
# # #
# # #
# # # pr = cProfile.Profile()
# # # # pr = cProfile.Profile(time.time)
# # # pr.enable()
# # # # start = time.time()
# # # foo(is_numpy)
# # # # end = time.time()
# # # # diff = end - start
# # # pr.disable()
# # # # times.append(diff)
# # # ps = pstats.Stats(pr).sort_stats('line')  # cumulative
# # # # ps.print_stats()
# # # # print(f'--{diff}')
# # # # print(time.get_clock_info('clock'))
# #
# # print(time.get_clock_info('clock'))
# print(time.get_clock_info('time'))
# print(time.get_clock_info('monotonic'))
# print(time.get_clock_info('perf_counter'))
# print(time.get_clock_info('process_time'))
# #
# #
# # #
# # # import os
# # # os.environ["MKL_NUM_THREADS"] = "1"
# # # os.environ["NUMEXPR_NUM_THREADS"] = "1"
# # # os.environ["OMP_NUM_THREADS"] = "1"
