#-----------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

from time import time
import numpy as np

def compute_julia(cr, ci, N, bound=1.5, lim=4., cutoff=1e6):
    ''' Pure Python calculation of the Julia set for a given `c` using NumPy
    array operations.
    '''
    c = cr + 1j * ci
    orig_err = np.seterr()
    np.seterr(over='ignore', invalid='ignore')
    julia = np.zeros((N, N), dtype=np.uint32)
    X, Y = np.ogrid[-bound:bound:N*1j, -bound:bound:N*1j]
    iterations = X + Y * 1j
    count = 1
    t0 = time()
    while not np.all(julia) and count < cutoff:
        mask = np.logical_not(julia) & (np.abs(iterations) >= lim)
        julia[mask] = count
        count += 1
        iterations = iterations**2 + c
    if count == cutoff:
        julia[np.logical_not(julia)] = count
    np.seterr(**orig_err)
    return julia, time() - t0
