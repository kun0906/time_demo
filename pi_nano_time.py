import os
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


import numpy as np
from sklearn.metrics import pairwise_distances

np.random.seed(42)

print(np.show_config())


def getGaussianGram(Xrow, Xcol, sigma, goFast=1):
    """ get kernel (Gaussian) gram matrix
    The Gram matrix K is deﬁned as $K_ij = K(X_i , X_j) over a (sub) sample X = {X _i}, i=1,...,,n
    Parameters
    ----------
    Xrow
    Xcol
    sigma
    goFast

    Returns
    -------

    """

    pr = cProfile.Profile(time.time)
    pr.enable()

    if goFast == 1:
        A1 = np.expand_dims(np.power(np.linalg.norm(Xrow, axis=1), 2), axis=1)  # change vector to matrix 100x1
        # A1 = np.power(np.linalg.norm(Xrow, axis=1), 2)    # vector: shape(n, ), matrix: (n, 1)
        A2 = -2 * np.matmul(Xrow, np.transpose(Xcol))
        B = np.power(np.linalg.norm(Xcol, axis=1), 2)
        K = np.add(np.add(A1, A2), np.transpose(B))
        K = np.exp(-K * 1 / sigma ** 2)

    else:
        # Dist = np.linalg.norm(Xrow - Xcol)  # it's wrong!
        # Dist= cdist(Xrow, Xcol, metric='euclidean')
        Dist = pairwise_distances(Xrow, Y=Xcol, metric='euclidean')
        K = np.exp(-np.power(Dist, 2) * 1 / sigma ** 2)

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    # ps.print_stats()

    return K


def foo(nums=50):
    s = 0
    is_numpy = 2
    if is_numpy==1:
        Xrow = np.ones((100, 20))
        X = np.ones((600, 20))
        for i in range(nums):
            s = np.matmul(X, Xrow.T)

        # del Xrow, X
    elif is_numpy==2:
        X = np.ones((600, 20))
        Xrow = np.ones((100, 20))
        getGaussianGram(X, Xrow, sigma=0.1)

    else:
        s = 0
        for i in range(10000000):
            s += i


def time_timing(name=''):
    start = time.time()

    foo()
    # time.sleep(1)

    end = time.time()

    return end - start


def ctime_timing(name=''):
    pr = cProfile.Profile(time.time)
    pr.enable()

    foo()
    # time.sleep(1)

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative

    return ps.total_tt


def process_timing(name=''):
    pr = cProfile.Profile(time.process_time)
    pr.enable()

    foo()
    # time.sleep(1)

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    # ps.print_stats()
    return ps.total_tt


def perf_counter_timing(name=''):
    pr = cProfile.Profile(time.perf_counter)
    pr.enable()

    foo()
    # time.sleep(1)

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative

    return ps.total_tt


n_repeats = 20

res = []
for i in range(n_repeats):
    res.append(time_timing())
print(f'time_time: {np.mean(res):.5f}+/-{np.std(res):.5f}')

res = []
for i in range(n_repeats):
    res.append(ctime_timing())
print(f'cprofile time: {np.mean(res):.5f}+/-{np.std(res):.5f}')

res = []
for i in range(n_repeats):
    res.append(process_timing())
print(f'cprofile process_time: {np.mean(res):.5f}+/-{np.std(res):.5f}')

res = []
for i in range(n_repeats):
    res.append(perf_counter_timing())
print(f'cprofile perf_counter: {np.mean(res):.5f}+/-{np.std(res):.5f}')
