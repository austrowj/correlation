from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

cxcov = Extension(
            "cxcov",
            ["cxcov.pyx"],
            extra_compile_args=['-O3','-msse3']
        )

setup(
    cmdclass = {'build_ext': build_ext},
    include_dirs = [numpy.get_include()],
    ext_modules = [cxcov]
)
