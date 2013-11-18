from libcpp.vector cimport vector
from cython.operator cimport dereference as deref

cdef extern from "particle.h":
    
    float _norm2 "norm2"(float x, float y, float z)

    cdef cppclass _Particle "Particle":
        _Particle()
        _Particle(float, float, float,
                 float, float, float,
                 float, float)
        float get_speed()
        float get_x()
    
def norm2(float x, float y, float z):
    cdef float pn = _norm2(x, y, z)
    return pn

cdef class Particle:

    cdef _Particle *_thisptr

    def __cinit__(self, x, y, z, vx, vy, vz, mass, charge):
        self._thisptr = new _Particle(x, y, z, vx, vy, vz, mass, charge)

    def __dealloc__(self):
        del self._thisptr

    cpdef float get_x(self):
        return self._thisptr.get_x()

    cpdef float get_speed(self):
        return self._thisptr.get_speed()


if __name__ == '__main__':
    import numpy as np
    assert np.allclose(norm2(1, 2, 3), np.sqrt(14.0))
