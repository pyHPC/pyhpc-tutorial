# --- Python std lib imports -------------------------------------------------
from time import time
import numpy as np

cdef float abs_sq(float zr, float zi):
    return zr * zr + zi * zi

cdef int kernel(float zr, float zi, float cr, float ci, float lim, double cutoff):
    cdef:
        int count = 0
        float lim_sq = lim * lim
    while abs_sq(zr, zi) < lim_sq and count < cutoff:
        zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
        count += 1
    return count

def compute_julia(float cr, float ci, int N, float bound=1.5, float lim=1000., double cutoff=1e6):
    cdef:
        int i, j
        float x, y
        unsigned int[:,::1] julia
        float[::1] grid
    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.array(np.linspace(-bound, bound, N), dtype=np.float32)
    t0 = time()
    for i in range(N):
        x = grid[i]
        for j in range(N):
            y = grid[j]
            julia[i,j] = kernel(x, y, cr, ci, lim, cutoff)
    return julia, time() - t0
