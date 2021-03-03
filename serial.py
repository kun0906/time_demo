
import time
from function import foo

def serial_func(n_repeats=5, is_numpy=False):
    """ Get the time taken on foo() function measured by time.time() and time.process_time()

    :param n_repeats:
    :param is_numpy:
    :return:
    """
    times = []
    process_times = []

    for i in range(n_repeats):
        start = time.time()
        foo(is_numpy)
        end = time.time()
        diff = end - start
        times.append(diff)

        start = time.process_time()
        foo(is_numpy)
        end = time.process_time()
        diff = end - start
        process_times.append(diff)

    res = [('time', times), ('process_time', process_times)]
    return res
