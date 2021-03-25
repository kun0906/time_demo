
import os
#
# # must set these before loading numpy:
# os.environ["OMP_NUM_THREADS"] = '1'  # export OMP_NUM_THREADS=4
# os.environ["OPENBLAS_NUM_THREADS"] = '1'  # export OPENBLAS_NUM_THREADS=4
# os.environ["MKL_NUM_THREADS"] = '1'  # export MKL_NUM_THREADS=6
# # os.environ["VECLIB_MAXIMUM_THREADS"] = '4' # export VECLIB_MAXIMUM_THREADS=4
# os.environ["NUMEXPR_NUM_THREADS"] = '1' # export NUMEXPR_NUM_THREADS=6

import time

import numpy as np
from threadpoolctl import threadpool_limits

def foo(is_numpy = True):
    """ if we use numpy or not

    :param is_numpy:
    :return:
    """
    if is_numpy:


        with threadpool_limits(limits=1, user_api='blas'):
            Xrow = np.ones((1000, 20))
            X = np.ones((6000, 20))
            s = np.matmul(X, Xrow.T)

        # Xrow = np.ones((1000, 20))
        # X = np.ones((600, 20))
        # s = np.matmul(X, Xrow.T)
    else:
        # don't use numpy array
        s = 0
        # time.sleep(0.001)
        for i in range(100000):
            s += i

    return s


is_numpy = True
print(f'is_numpy={is_numpy}')
# sp = ' '
# def format_str(s, sp=' ', l=20):
#     s += sp* (l-len(s))
#     return s
for i in range(10):
    start = time.time()
    foo(is_numpy)
    end = time.time()
    diff = end - start
    name = 'wall_clock'
    print(f'{name:20}: {diff}')

for i in range(10):
    # 2.1 process_time()
    start = time.process_time()
    foo(is_numpy)
    end = time.process_time()
    diff2 = end - start
    name = 'process_time'
    print(f'{name:20}: {diff2}')

for i in range(10):
    start = time.time()
    foo(is_numpy)
    end = time.time()
    diff = end - start
    name = 'wall_clock'
    print(f'{name:20}: {diff}')
#
# for i in range(10):
#     start = time.perf_counter()
#     foo(is_numpy)
#     end = time.perf_counter()
#     diff = end - start
#     print(f'perf_counter: {diff}')
#     # print(f'wall_clock-process_time: {diff-diff2}\n')
