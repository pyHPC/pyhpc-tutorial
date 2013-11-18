# from cython.view import array as cvarray
cimport cython
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt

DEF _LEN = 3

cdef class Particle:

    cdef:
        float *psn, *vel
        public float mass, charge

    def __cinit__(self):
        # allocate the psn and vel arrays on the heap.
        self.psn = <float*>malloc(_LEN * sizeof(float))
        self.vel = <float*>malloc(_LEN * sizeof(float))
        if not self.psn or not self.vel:
            raise MemoryError("Cannot allocate memory.")

    def __init__(self, psn=None, vel=None, mass=0.0, charge=0.0):
        # called after __cinit__() -- initialize all data.
        zeros = (0.0,)*_LEN
        psn = psn or zeros
        vel = vel or zeros
        for i in range(_LEN):
            self.psn[i] = psn[i]
            self.vel[i] = vel[i]
        self.mass = mass
        self.charge = charge

    def __dealloc__(self):
        # called when cleaning up the object; free malloc'd memory.
        if self.psn:
            free(self.psn); self.psn == NULL
        if self.vel:
            free(self.vel); self.vel == NULL

    property position:

        def __get__(self):
            return tuple(self.psn[i] for i in range(_LEN))

        def __set__(self, it):
            for i in range(_LEN):
                self.psn[i] = it[i]

    property velocity:

        def __get__(self):
            return tuple(self.vel[i] for i in range(_LEN))

        def __set__(self, it):
            for i in range(_LEN):
                self.vel[i] = it[i]

    property momentum:

        "Particle object's momentum."

        def __get__(self):
            return tuple(self.vel[i] * self.mass for i in range(_LEN))

