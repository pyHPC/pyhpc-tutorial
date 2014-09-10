'''
Fibonnaci exercise -- the "Hello World!" of Cython.
---------------------------------------------------

0. The `pyfib.py` file is a pure-python module which defines just the `pyfib()`
function (named so we can distinguish it from the sped-up versions of `fib()`).

For baseline timings, lets time its performance in the IPython interpreter:

    $ ipython --no-banner
    
    In [1]: from pyfib import pyfib

    In [2]: %timeit pyfib(10)
    1000000 loops, best of 3: 1.52 us per loop

So the pure-python version of this function takes 1.5 microseconds to run.  We
will speed this up using Cython.

1. The fib.pyx file has a function `fib()` that has the same function body as
the `pyfib()` function earlier.  This is also valid Cython code.  We will
compile this file into a Python extension module and see what kind of speedup
we get.

The file `setup_fib.py` tells Python how to automatically compile the
`fib.pyx` file into an extension module.  From the commandline, run the
following command to generate an extsion module:

    $ python setup_fib.py build_ext -i

If successful, you will see a shared object file, `fib.so`, in the current
directory.

2. You can load this extension module in an interactive interpreter (here,
IPython), like so:

    $ ipython --no-banner
    
    In [1]: from fib import fib

    In [2]: fib(10)
    Out[2]: 55

To get quick timing information, do the following:

    In [3]: %timeit fib(10)
    1000000 loops, best of 3: 519 ns per loop

3. Add type information to the fib function like in the slide material.  Re-run
the "python setup_fib.py ..." command to re-compile the extension module.
Re-run the timing command in IPython, and see what kind of speedup you get.

See the `fib_solution.pyx` file for the solution to this exercise.

'''


def pyfib(n):
    a,b = 0,1
    for i in range(n):
        a, b = a+b, a
    return a
