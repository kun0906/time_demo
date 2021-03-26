# from func_timeout import func_set_timeout


FUNC_TIMEOUT = 3* 60


# @func_set_timeout(FUNC_TIMEOUT)  # seconds
def foo(is_numpy = True):
    """ if we use numpy or not

    :param is_numpy:
    :return:
    """
    if is_numpy:
        import numpy as np
        from threadpoolctl import threadpool_limits

        # with threadpool_limits(limits=1, user_api=None):
        #     Xrow = np.ones((100, 20))
        #     X = np.ones((600, 20))
        #     s = np.matmul(X, Xrow.T)

        Xrow = np.ones((100, 20))
        X = np.ones((600, 20))
        for i in range(100):   # 1000
            s = np.matmul(X, Xrow.T)
    else:
        # don't use numpy array
        s = 0
        # time.sleep(0.001)
        for i in range(100000):
            s += i

    return s
