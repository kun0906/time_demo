

import numpy as np

def foo(is_numpy = True):
    """ if we use numpy or not

    :param is_numpy:
    :return:
    """
    if is_numpy:
        Xrow = np.ones((100, 5))
        X = np.ones((600, 5))
        s = np.matmul(X, Xrow.T)
    else:
        # don't use numpy array
        s = 0
        # time.sleep(0.001)
        for i in range(100000):
            s += i

    return s
