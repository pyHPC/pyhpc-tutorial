cimport cython
from libc.math cimport sqrt

DEF _LEN = 3

cdef float magnitude(float *vec):
    cdef float mag = 0.0
    cdef int idx
    for idx in range(_LEN):
        mag += vec[idx]*vec[idx]
    return sqrt(mag)

cdef class Particle:

    cdef:
        float psn[_LEN]
        float vel[_LEN]
        public float mass, charge

    def __init__(self, psn=None, vel=None, mass=0.0, charge=0.0):
        zeros = (0.0,)*_LEN
        psn = psn or zeros
        vel = vel or zeros
        for i in range(_LEN):
            self.psn[i] = psn[i]
            self.vel[i] = vel[i]
        self.mass = mass
        self.charge = charge

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

    property speed:

        def __get__(self):
            return magnitude(self.vel)

    property direction:

        def __get__(self):
            cdef float spd = self.speed
            return tuple(self.vel[i] / spd for i in range(_LEN))

