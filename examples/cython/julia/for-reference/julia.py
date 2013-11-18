#-----------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

'''
julia.py

Compute and plot the Julia set.

This provides a self-contained---if somewhat contrived---example for comparing
the runtimes between pure Python, Numpy, Cython, and Cython-wrapped C versions
of the julia set calculation.

It is meant to be run from the command line; run

    $ python julia.py -h

for details.

'''

# --- Python / Numpy imports -------------------------------------------------
import numpy as np
import pylab as pl

# --- Import the various julia set computation modules -----------------------
import julia_pure_python
import julia_cython_solution as julia_cython
# import julia_cython
import julia_numpy
# import julia_multiprocessing_solution as julia_multiprocessing

def printer(label, runtime, speedup):
    ''' Given a label, the total runtime in seconds, and a speedup value,
    prints things nicely to stdout.
    '''
    from sys import stdout
    print "{}:".format(label.strip())
    fs =  "    {:.<15s} {: >6.2g}"
    print fs.format("runtime (s)", runtime)
    print fs.format("speedup", speedup)
    print
    stdout.flush()

# some good c values:
# (-0.1 + 0.651j)
# (-0.4 + 0.6j) 
# (0.285 + 0.01j)

def plot_julia(kwargs, compute_julia):
    ''' Given parameters dict in `kwargs` and a function to compute the Julia
    set (`compute_julia`), plots the resulting Julia set with appropriately
    labeled axes.
    '''
    kwargs = kwargs.copy()

    def _plotter(kwargs):
        bound = kwargs['bound']
        julia, _ = compute_julia(**kwargs)
        julia = np.log(julia)
        pl.imshow(julia, 
                  interpolation='nearest',
                  extent=(-bound, bound)*2)
        pl.colorbar()
        title = r"Julia set for $C={0.real:5.3f}+{0.imag:5.3f}i$ $[{1}\times{1}]$"
        pl.title(title.format(kwargs['c'], kwargs['N']))
        pl.xlabel("$Re(z)$")
        pl.ylabel("$Im(z)$")

    pl.figure(figsize=(14, 12))

    cvals = [0.285+0.01j, -0.1+0.651j, -0.4+0.6j, -0.8+0.156j]
    subplots = ['221',    '222',       '223',     '224'      ]

    for c, sp in zip(cvals, subplots):
        kwargs.update(c=c)
        pl.subplot(sp)
        _plotter(kwargs)

    pl.show()

def compare_runtimes(kwargs):
    ''' Given a parameter dict `kwargs`, runs different implementations of the
    Julia set computation and compares the runtimes of each.
    '''

    ref_julia, python_time = julia_pure_python.compute_julia(**kwargs)
    printer("Python only", python_time, 1.0)

    _, numpy_time = julia_numpy.compute_julia(**kwargs)
    # assert np.allclose(ref_julia, _)
    printer("Python only + Numpy expressions", numpy_time,
            python_time / numpy_time)

    _, cython_kernel_time = julia_pure_python.compute_julia(
                                    kernel=julia_cython.kernel, **kwargs)
    assert np.allclose(ref_julia, _)
    printer("Python + cythonized kernel", cython_kernel_time, 
            python_time / cython_kernel_time)

    _, mp_time = julia_multiprocessing.compute_julia_block(kernel=julia_pure_python.kernel, **kwargs)
    assert np.allclose(ref_julia, _)
    printer("Multiprocessing + Python kernel", mp_time, python_time / mp_time)

    _, mp_time = julia_multiprocessing.compute_julia_block(kernel=julia_cython.kernel, **kwargs)
    assert np.allclose(ref_julia, _)
    printer("Multiprocessing + cythonized kernel", mp_time, python_time / mp_time)

    _, cython_no_opt_time = julia_cython.compute_julia_no_opt(**kwargs)
    assert np.allclose(ref_julia, _)
    printer("All Cython, no optimizations", cython_no_opt_time, 
            python_time / cython_no_opt_time)

    _, cython_opt_time = julia_cython.compute_julia_opt(**kwargs)
    assert np.allclose(ref_julia, _)
    printer("All Cython, Numpy optimizations", cython_opt_time,
            python_time / cython_opt_time)

    _, ext_opt_time = julia_cython.compute_julia_ext(**kwargs)
    assert np.allclose(ref_julia, _)
    printer("All C version, wrapped with Cython", ext_opt_time,
            python_time / ext_opt_time)

def main(args):
    ''' The main entry point; branches on whether `args.action` is "plot" or
    "compare".
    '''
    bound = 1.5
    kwargs = dict(cr=0.285, ci=0.01,
                  N=args.N,
                  bound=bound)

    if args.action == 'plot':
        plot_julia(kwargs, julia_cython.compute_julia_ext)
    elif args.action == 'compare':
        compare_runtimes(kwargs)

description = """ Explore the performance characteristics of Cython and Numpy
when computing the Julia set."""

help_arg_n = """ The number of grid points in each dimension; larger for more
resolution.  (default 100)) """

help_arg_a = """ Either *plot* an approximation of a Julia set with resolution
N (default), or *compare* the runtimes for different implementations.) """

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=description)

    parser.add_argument('-N', type=int, default=200, help=help_arg_n)
    parser.add_argument('-a', '--action', type=str, 
                        default='plot', 
                        choices=('plot', 'compare'),
                        help=help_arg_a)

    args = parser.parse_args()
    main(args)
