
import time
from function import foo

def serial_func(n_repeats=5):

    times = []

    process_times = []

    for i in range(n_repeats):
        start = time.time()
        foo()
        end = time.time()
        diff = end - start
        times.append(diff)

        start = time.process_time()
        foo()
        end = time.process_time()
        diff = end - start
        process_times.append(diff)

    res = [('time', times), ('process_time', process_times)]
    return res
