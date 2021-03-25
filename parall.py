import cProfile
import time

from joblib import Parallel, delayed

import pstats
from function import foo


def _timing(name, is_numpy):
    if name == 'time':
        ##########
        start = time.time()
        foo(is_numpy)
        end = time.time()
        diff = end - start

    elif name == 'cprofile_time':  # time.time()
        pr = cProfile.Profile(time.time)
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        diff = ps.total_tt

    elif name == 'cprofile_default_time':
        # python3.6-3.7 using gettimeofday() as default timer, python3.8+  using perf_counter()
        pr = cProfile.Profile()
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        diff = ps.total_tt

    elif name == 'process_time':
        ###########
        start = time.process_time()
        foo(is_numpy)
        end = time.process_time()
        diff = end - start

    elif name == 'cprofile_process_time':  # time.process_time()
        pr = cProfile.Profile(time.process_time)
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        diff = ps.total_tt

    elif name == 'perf_counter_time':  # time.perf_counter()
        ###########
        start = time.perf_counter()
        foo(is_numpy)
        end = time.perf_counter()
        diff = end - start

    elif name == 'cprofile_perf_counter':  # time.perf_counter()
        pr = cProfile.Profile(time.perf_counter)
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        diff = ps.total_tt

    else:
        raise NotImplementedError

    return diff


def timing(name, n_repeats, is_numpy):
    res = []
    for i in range(n_repeats):
        diff = _timing(name, is_numpy)
        res.append(diff)

    return name, res

def parallel_func(n_repeats=5, n_jobs=2, is_numpy=False):
    """ Apply for n_jobs (=2) CPUs to run the timing function (time.time() and time.process_time()).
        Each time function will be executed 10 times on one CPU.

    :param n_repeats:
    :param n_jobs:
    :param is_numpy:
    :return:
    """

    names = ['time', 'cprofile_time',
             'process_time', 'cprofile_process_time',
             'perf_counter_time', 'cprofile_perf_counter',
             'cprofile_default_time',]
    # names = ['time']
    # Apply for n_jobs (=2) CPUs to run the timing function. Each time function will be executed 10 times on one CPU
    print(f'n_jobs: {n_jobs}')  # batch_size='auto', temp_folder=None
    # with Parallel(n_jobs=n_jobs, verbose=0, backend='loky') as parallel:
    with Parallel(n_jobs=n_jobs, verbose=0, backend='multiprocessing') as parallel:    # multiprocessing
        res = parallel(delayed(timing)(name_, n_repeats, is_numpy) for name_ in names)

    return res
