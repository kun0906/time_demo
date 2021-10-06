"""
https://betterscientificsoftware.github.io/python-for-hpc/interrogating-numpy/

"""
import pprint
from distutils import sysconfig
cfg = sysconfig.get_config_vars()
pprint.pprint(cfg)

import numpy.distutils
# from numpy.distutils.system_info import *
# np_config_vars = numpy.distutils.unixccompiler.sysconfig.get_config_vars()
# np_config_vars = numpy.distutils.misc_util.get_info()

pprint.pprint(np_config_vars)


from distutils import sysconfig
sysconfig.get_config_vars()

import sysconfig
print(sysconfig.get_config_vars())
