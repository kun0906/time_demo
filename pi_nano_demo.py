# os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4
# os.environ["OPENBLAS_NUM_THREADS"] = "1"  # export OPENBLAS_NUM_THREADS=4
# os.environ["MKL_NUM_THREADS"] = "1"  # export MKL_NUM_THREADS=6
# os.environ["VECLIB_MAXIMUM_THREADS"] = "1"  # export VECLIB_MAXIMUM_THREADS=4
# os.environ["NUMEXPR_NUM_THREADS"] = "1"  # export NUMEXPR_NUM_THREADS=6
import cProfile
import time
from sys import getsizeof

import numpy as np

import pstats

T = 1024*1024*1024  # GB
# os.environ['NUMPY_EXPERIMENTAL_ARRAY_FUNCTION'] = '0'
# print(np.__config__.show())

def foo(m=100, d=20):
	pr = cProfile.Profile(time.perf_counter)
	pr.enable()

	X = np.ones((5000, d))
	Xrow = np.ones((m, d))
	# print(getsizeof(Xrow), X.nbytes)
	for i in range(10):
		s = np.matmul(X, Xrow.T)    # 5000 x m
	print(getsizeof(Xrow)/T, Xrow.nbytes/T, X.nbytes/T, s.nbytes / T)
	# del Xrow, X
	pr.disable()
	ps = pstats.Stats(pr).sort_stats('line')  # cumulative
	# ps.print_stats()

	return ps.total_tt


def main(m=1000, n_repeats=10):
	res = []
	for i in range(n_repeats):
		res.append(foo(m, d=5))

	# print(f'{np.mean(res):.5f}+/-{np.std(res):.5f}')
	return f'{np.mean(res):.5f}', f'{np.std(res):.5f}'


if __name__ == '__main__':
	res = []
	with open('a.txt', 'w') as f:
		for m in [600, 1000, 2000, 5000, 10000, 100000, 300000]:
			# 600*8*5 / T
			mu, std = main(m, n_repeats=1)
			s = f'{m * 8 * 5 / T:.5f}GB'
			s1 = f'{5000 * m * 8/ T:.5f}GB' # X * Xrow.T and the shape is (5000, m)
			vs = (m, mu, std, s, s1)
			print(vs)
			# res.append(vs)
			f.write(','.join([str(v) for v in vs]) + '\n')
			time.sleep(5)  # sleep 5 seconds



