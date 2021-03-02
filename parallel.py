import time

from joblib import Parallel, delayed

from function import foo


def parallel_func(n_repeats=5, n_jobs=10):
    def _timing(name):
        diff = 0.0
        if name == 'time':
            ###########
            start = time.time()
            foo()
            end = time.time()
            diff = end - start

        elif name == 'process_time':
            ###########
            start = time.process_time()
            foo()
            end = time.process_time()
            diff = end - start

        return diff

    def timing(name):
        res = []
        for i in range(n_repeats):
            diff = _timing(name)
            res.append(diff)

        return name, res

    names = ['time', 'process_time']
    with Parallel(n_jobs=n_jobs, verbose=0, backend='loky', pre_dispatch=1, batch_size=1, temp_folder=None) as parallel:
        res = parallel(delayed(timing)(name_) for name_ in names)

    return res
