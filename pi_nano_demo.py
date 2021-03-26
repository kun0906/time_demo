import os
os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4
os.environ["OPENBLAS_NUM_THREADS"] = "1"  # export OPENBLAS_NUM_THREADS=4
os.environ["MKL_NUM_THREADS"] = "1"  # export MKL_NUM_THREADS=6
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"  # export VECLIB_MAXIMUM_THREADS=4
os.environ["NUMEXPR_NUM_THREADS"] = "1"  # export NUMEXPR_NUM_THREADS=6
import cProfile
import time
import pstats
import numpy as np
print(np.__config__.show())

def foo(m=100, d=20):
    pr = cProfile.Profile(time.time)
    pr.enable()

    s = 0
    is_numpy = True
    if is_numpy:
        X = np.ones((600, d))
        Xrow = np.ones((m, d))
        for i in range(1):
            s = np.matmul(X, Xrow.T)

        del Xrow, X
    else:
        s = 0
        for i in range(10000000):
            s += i

    pr.disable()
    ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    ps.print_stats()

    return ps.total_tt

n_repeats = 1
res = []
for i in range(n_repeats):
    foo(m=50, d=5)
    foo(m=2000, d=5)
    res.append(foo(m=2000, d=20))
print(f'{np.mean(res):.5f}+/-{np.std(res):.5f}')
