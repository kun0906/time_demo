"""
    https://stackoverflow.com/questions/17843622/benchmarking-cpu-time-bigger-than-wall-time
    If a computation requires two seconds of processor time, then two processors can (ideally) complete it in one second.
    Hence a two-processor system has two CPU seconds for every wall-clock second. Even if you do not use multi-
    threading explicitly in your process, a library you use or the operating system may use multiple processors to
    perform work for your process.

    https://stackoverflow.com/questions/27863717/why-is-time-clock-giving-a-greater-elapsed-time-than-time-time
    The kernel accounts for CPU time measuring all cores. If multiple cores run during the same second
    then you spent multiple CPU seconds during that second.
"""
import cProfile
import time

import pstats
from function import foo


def serial_func(n_repeats=5, is_numpy=False):
    """ Get the time taken on foo() function measured by time.time() and time.process_time()

    :param n_repeats:
    :param is_numpy:
    :return:
    """
    # time.sleep(1)
    times = []
    cprofile_times = []

    process_times = []
    cprofile_process_times = []

    perf_counter_times = []
    cprofile_default_times = []
    cprofile_perf_counters = []

    times1 = []
    cprofile_times1 = []

    times2 = []
    cprofile_times2 = []

    for i in range(n_repeats):
        # 1.1 time.time()
        start = time.time()
        foo(is_numpy)
        end = time.time()
        diff = end - start
        times.append(diff)

    for i in range(n_repeats):
        # 1.2 cprofile_time()
        pr = cProfile.Profile(time.time)
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        cprofile_times.append(ps.total_tt)

    for i in range(n_repeats):
        # 1.3.
        # python3.6-3.7 using gettimeofday() as default timer, python3.8+  using perf_counter()
        #  gettimeofday() returns the wall-clock time
        pr = cProfile.Profile()
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        cprofile_default_times.append(ps.total_tt)

    # # ----------
    # for i in range(n_repeats):
    #     # 1.1 time.time()
    #     start = time.time()
    #     foo(is_numpy)
    #     end = time.time()
    #     diff = end - start
    #     times1.append(diff)
    #
    # for i in range(n_repeats):
    #     # 1.2 cprofile_time()
    #     pr = cProfile.Profile(time.time)
    #     pr.enable()
    #     foo(is_numpy)
    #     pr.disable()
    #     ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    #     # ps.print_stats()
    #     cprofile_times1.append(ps.total_tt)

    for i in range(n_repeats):
        # 2.1 process_time()
        start = time.process_time()
        foo(is_numpy)
        end = time.process_time()
        diff = end - start
        process_times.append(diff)

    for i in range(n_repeats):
        # 2.2 cprofile_process_time()
        pr = cProfile.Profile(time.process_time)
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        cprofile_process_times.append(ps.total_tt)

    for i in range(n_repeats):
        # 3.1. perf_counter()
        start = time.perf_counter()
        foo(is_numpy)
        end = time.perf_counter()
        diff = end - start
        perf_counter_times.append(diff)

    for i in range(n_repeats):
        # 3.2 cprofile use the default time function: perf_counter()
        pr = cProfile.Profile(time.perf_counter)
        pr.enable()
        foo(is_numpy)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('line')  # cumulative
        # ps.print_stats()
        cprofile_perf_counters.append(ps.total_tt)



    # #----------
    # for i in range(n_repeats):
    #     # 1.1 time.time()
    #     start = time.time()
    #     foo(is_numpy)
    #     end = time.time()
    #     diff = end - start
    #     times2.append(diff)
    #
    # for i in range(n_repeats):
    #     # 1.2 cprofile_time()
    #     pr = cProfile.Profile(time.time)
    #     pr.enable()
    #     foo(is_numpy)
    #     pr.disable()
    #     ps = pstats.Stats(pr).sort_stats('line')  # cumulative
    #     # ps.print_stats()
    #     cprofile_times2.append(ps.total_tt)

    res = [
        ('time', times), ('cprofile_time', cprofile_times),
        # ('time1', times1), ('cprofile_time1', cprofile_times1),
        ('process_time', process_times), ('cprofile_process_time', cprofile_process_times),
        ('perf_counter_time', perf_counter_times),
        ('cprofile_perf_counters', cprofile_perf_counters),
        # ('time2', times2), ('cprofile_time2', cprofile_times2)
        ('cprofile_default_time', cprofile_default_times),
    ]

    return res
