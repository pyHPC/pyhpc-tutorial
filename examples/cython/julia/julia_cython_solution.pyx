#-----------------------------------------------------------------------------
# Copyright (c) 2012, 2013, Enthought, Inc.
# All rights reserved.  Distributed under the terms of the 2-clause BSD
# licence.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

# --- Python std lib imports -------------------------------------------------
from time import time
import numpy as np

# --- Cython cimports --------------------------------------------------------
cimport cython
from libc.stdint cimport uint32_t, int32_t
from cython.parallel cimport prange

# --- Ctypedefs --------------------------------------------------------
ctypedef float     real_t
ctypedef uint32_t  uint_t
ctypedef int32_t   int_t

#-----------------------------------------------------------------------------
# Cython functions
#-----------------------------------------------------------------------------
cdef real_t abs_sq(real_t zr, real_t zi) nogil:
    return zr * zr + zi * zi

cdef uint_t kernel(real_t zr, real_t zi,
                   real_t cr, real_t ci,
                   real_t lim, real_t cutoff) nogil:
    cdef:
        uint_t count = 0
        real_t lim_sq = lim * lim
        
    while abs_sq(zr, zi) < lim_sq and count < cutoff:
        zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
        count += 1
    return count

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_julia(real_t cr, real_t ci,
                  uint32_t N, real_t bound=1.5,
                  real_t lim=1000., real_t cutoff=1e6):
    cdef:
        uint_t[:,::1] julia 
        real_t[::1] grid
        int i, j
        real_t x, y
        
    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.asarray(np.linspace(-bound, bound, N), dtype=np.float32)
    t0 = time()
    for i in range(N):
        x = grid[i]
        for j in range(N):
            y = grid[j]
            julia[i,j] = kernel(x, y, cr, ci, lim, cutoff)
    return julia, time() - t0

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_julia_parallel(real_t cr, real_t ci,
                           uint_t N, real_t bound=1.5,
                           real_t lim=1000., real_t cutoff=1e6):
    cdef:
        uint_t[:,::1] julia 
        real_t[::1] grid
        int_t i, j
        real_t x

    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.asarray(np.linspace(-bound, bound, N), dtype=np.float32)
    t0 = time()
    for i in prange(N, nogil=True):
        x = grid[i]
        for j in range(N):
            julia[i,j] = kernel(x, grid[j], cr, ci, lim, cutoff)
    return julia, time() - t0
