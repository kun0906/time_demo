

import numpy as np

# @scalene_redirect_profile
# @profile
def foo(is_numpy_arr = True):

    if is_numpy_arr:
        Xrow = np.ones((100, 5))
        X = np.ones((600, 5))
        s = np.matmul(X, Xrow.T)
    else:
        # don't use numpy array
        s = 0
        # time.sleep(0.001)
        for i in range(100000):
            s += i
        del s

    return s
