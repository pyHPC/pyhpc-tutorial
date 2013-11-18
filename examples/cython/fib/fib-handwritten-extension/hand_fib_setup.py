from distutils.core import setup, Extension

ext = Extension(name='hand_fib', sources=['hand_fib.c'], extra_compile_args=['-O3'])

setup(name="hand_fib", ext_modules=[ext])
