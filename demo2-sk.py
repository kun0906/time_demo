import cProfile
import os
#
# # must set these before loading numpy:
# os.environ["OMP_NUM_THREADS"] = '1'  # export OMP_NUM_THREADS=4
# os.environ["OPENBLAS_NUM_THREADS"] = '1'  # export OPENBLAS_NUM_THREADS=4
# os.environ["MKL_NUM_THREADS"] = '1'  # export MKL_NUM_THREADS=6
# os.environ["VECLIB_MAXIMUM_THREADS"] = '1' # export VECLIB_MAXIMUM_THREADS=4
# os.environ["NUMEXPR_NUM_THREADS"] = '1' # export NUMEXPR_NUM_THREADS=6

import os

import sklearn

os.environ["OMP_NUM_THREADS"] = "1" # export OMP_NUM_THREADS=4
os.environ["OPENBLAS_NUM_THREADS"] = "1" # export OPENBLAS_NUM_THREADS=4
os.environ["MKL_NUM_THREADS"] = "1" # export MKL_NUM_THREADS=6
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" # export VECLIB_MAXIMUM_THREADS=4
os.environ["NUMEXPR_NUM_THREADS"] = "1" # export NUMEXPR_NUM_THREADS=6

from pprint import pprint

from threadpoolctl import threadpool_info, threadpool_limits
from joblib import parallel, Parallel, delayed
import numpy as np
# print(np.show_config())
import time

import pstats
from sklearn.metrics import pairwise_distances

# pprint(threadpool_info())
print('**')
print(sklearn.get_config())

def getGaussianGram(Xrow, Xcol, sigma, goFast=0):
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

    return K


n_repeats = 1
def foo(idx):

    print(f"idx={idx}")

    cprofile_process_times= []
    Xrow = np.ones((600, 20))
    for i in range(n_repeats):
        # 2.2 cprofile_process_time()
        pr = cProfile.Profile(time.process_time, builtins=False, subcalls=True)
        pr.enable()
        getGaussianGram(Xrow, Xrow, sigma=0.5)
        np.matmul(Xrow, Xrow.transpose())
        np.matmul(Xrow, Xrow.transpose())
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        ps.print_stats()
        cprofile_process_times.append(ps.total_tt)

        # # 2.2 cprofile_process_time()
        # pr = cProfile.Profile(time.process_time)
        # pr.enable()
        # getGaussianGram(Xrow, Xrow, sigma=0.5)
        # np.matmul(Xrow, Xrow.transpose())
        # pr.disable()
        # ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # # ps.print_stats()
        # cprofile_process_times.append(ps.total_tt)


    print(f'idx={idx}', np.mean(cprofile_process_times), np.std(cprofile_process_times))#, cprofile_process_times)

    return cprofile_process_times


combs=[0, 1, 2, 3,4, 5, 6,7]
print('*****serial')

for i in combs:
    foo(i)

print('*****parallel')
# pre_dispatch='2 * n_jobs', batch_size='auto', temp_folder=None
with Parallel(n_jobs=2, verbose=0, backend='loky') as parallel:
    res = parallel(delayed(foo)(i) for i in combs)



# #
# # print('scipy')
# # import scipy
# # pprint(threadpool_info())
#
# flg = 0
# if flg:
#     import os
#
#     # must set these before loading numpy:
#     os.environ["OMP_NUM_THREADS"] = '8'  # export OMP_NUM_THREADS=4
#     os.environ["OPENBLAS_NUM_THREADS"] = '8'  # export OPENBLAS_NUM_THREADS=4
#     os.environ["MKL_NUM_THREADS"] = '8'  # export MKL_NUM_THREADS=6
#     # os.environ["VECLIB_MAXIMUM_THREADS"] = '4' # export VECLIB_MAXIMUM_THREADS=4
#     # os.environ["NUMEXPR_NUM_THREADS"] = '4' # export NUMEXPR_NUM_THREADS=6
#
#     import numpy as np
#     print(np.show_config())
#
#     with threadpool_limits(limits=1, user_api='blas'):
#         # In this block, calls to blas implementation (like openblas or MKL)
#         # will be limited to use only one thread. They can thus be used jointly
#         # with thread-parallelism.
#         a = np.random.randn(1000, 1000)
#         a_squared = a @ a
# #
# # flg = 2
# # if flg ==1:
# #     print('numpy')
# #     pprint(threadpool_info())
# #
# # elif flg == 2:
# #     print('sklearn')
# #     import sklearn
# #     pprint(threadpool_info())
# # else:
# #     print('scipy')
# #     import scipy
# #     pprint(threadpool_info())
#
#
#
#
