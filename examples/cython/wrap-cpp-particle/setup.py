from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext = Extension("wrap_particle", ["wrap_particle.pyx", "particle.cpp"], language="c++")

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [ext],
)
