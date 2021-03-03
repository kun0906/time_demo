import time

from joblib import Parallel, delayed

from function import foo


def parallel_func(n_repeats=5, n_jobs=2, is_numpy=False):
    """ Apply for n_jobs (=2) CPUs to run the timing function (time.time() and time.process_time()).
        Each time function will be executed 10 times on one CPU.

    :param n_repeats:
    :param n_jobs:
    :param is_numpy:
    :return:
    """
    def _timing(name):

        if name == 'time':
            ###########
            start = time.time()
            foo(is_numpy)
            end = time.time()
            diff = end - start

        elif name == 'process_time':
            ###########
            start = time.process_time()
            foo(is_numpy)
            end = time.process_time()
            diff = end - start

        else:
            raise NotImplementedError

        return diff

    def timing(name):
        res = []
        for i in range(n_repeats):
            diff = _timing(name)
            res.append(diff)

        return name, res

    names = ['time', 'process_time']
    # Apply for n_jobs (=2) CPUs to run the timing function. Each time function will be executed 10 times on one CPU
    with Parallel(n_jobs=n_jobs, verbose=0, backend='loky', pre_dispatch=1, batch_size=1, temp_folder=None) as parallel:
        res = parallel(delayed(timing)(name_) for name_ in names)

    return res
