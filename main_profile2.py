"""
    profile

    http://mitrocketscience.blogspot.com/2018/11/automatic-mulit-threading-with-python.html
     numpy vector operations are automatically parallelized if numpy is linked against certain libraries,
     e.g. openBLAS or MKL, during compilation. Those linear algebra libraries will automatically use the max
     number of available cores (or if your processor is HT, 2x number of physical cores) for matrix operations.

"""
import os
#
# # must set these before loading numpy:
# os.environ["OMP_NUM_THREADS"] = '1'  # export OMP_NUM_THREADS=4
# os.environ["OPENBLAS_NUM_THREADS"] = '1'  # export OPENBLAS_NUM_THREADS=4
# os.environ["MKL_NUM_THREADS"] = '1'  # export MKL_NUM_THREADS=6
# os.environ["VECLIB_MAXIMUM_THREADS"] = '1' # export VECLIB_MAXIMUM_THREADS=4
# os.environ["NUMEXPR_NUM_THREADS"] = '1' # export NUMEXPR_NUM_THREADS=6



from pprint import pprint
from threadpoolctl import threadpool_info, threadpool_limits
# pprint(threadpool_info())
from joblib import parallel
import numpy as np
# print(np.show_config())

from parall import parallel_func
from serial import serial_func


pprint(threadpool_info())
def show_data(res, name=''):
    from matplotlib import pyplot as plt
    plt.close('all')

    for i, (name_, vs_) in enumerate(res):
        plt.plot(vs_, label=name_)

    plt.title(name)
    plt.legend(loc = 'upper right')

    out_file = f'result/{name}.png'
    if not os.path.exists(os.path.dirname(out_file)):
        os.makedirs(os.path.dirname(out_file))
    plt.savefig(out_file)
    # plt.show()


def main(is_numpy=False):
    """ Get the time taken on foo() function measured by time.time() and time.process_time()
    """

    pprint(threadpool_info())
    print('**')

    n_repeats = 100

    print('\nserial')
    serial_res = serial_func(n_repeats, is_numpy)
    for i, (name_, vs_) in enumerate(serial_res):
        if i % 2 == 0 and i < 10:
            print(''.join(['-'] * 155))
        # print(f'{name_:25}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}', [f'{v:.5f}' for v in vs_])
        print(f'{name_:25}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}')
        if name_ == 'cprofile_default_time':  print(''.join(['-'] * 155))

    print('\nparallel')
    parallel_res = parallel_func(n_repeats, n_jobs=3, is_numpy=is_numpy)
    for i, (name_, vs_) in enumerate(parallel_res):
        if i % 2 == 0 and i < 10:
            print(''.join(['-'] * 155))
        # print(f'{name_:25}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}', [f'{v:.5f}' for v in vs_])
        print(f'{name_:25}: {np.mean(vs_):.5f}+/-{np.std(vs_):.5f}')
        if name_ == 'cprofile_default_time':  print(''.join(['-'] * 155))


    show_data(serial_res, name=f'serial(using numpy({is_numpy}))')
    show_data(parallel_res, name=f'parallel(using numpy({is_numpy}))')

if __name__ == '__main__':
    print('===========================================================================')
    print('1 ***use numpy array')
    main(is_numpy=True)

    print('\n===========================================================================')
    print('2 ***don\'t use numpy array')
    main(is_numpy=False)
