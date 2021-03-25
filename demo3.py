
flg =1
if flg:

    import os

    # must set these before loading numpy:
    # os.environ["OMP_NUM_THREADS"] = '1'  # export OMP_NUM_THREADS=4
    # os.environ["OPENBLAS_NUM_THREADS"] = '1'  # export OPENBLAS_NUM_THREADS=4
    # os.environ["MKL_NUM_THREADS"] = '1'  # export MKL_NUM_THREADS=6
    # # os.environ["VECLIB_MAXIMUM_THREADS"] = '4' # export VECLIB_MAXIMUM_THREADS=4
    # os.environ["NUMEXPR_NUM_THREADS"] = '1'  # export NUMEXPR_NUM_THREADS=6

    # import numpy as np
    #
    # a = np.ones((4096, 4096))
    # a.dot(a)

    import numpy as np
    from threadpoolctl import threadpool_limits

    with threadpool_limits(limits=1, user_api=None):
        a = np.ones((4096, 4096))
        a.dot(a)

else:
    import numpy as np
    a = np.ones((4096, 4096))
    a.dot(a)