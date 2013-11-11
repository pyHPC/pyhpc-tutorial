from petsc4py.PETSc cimport Vec,  PetscVec
from petsc4py.PETSc cimport DA,   PetscDM
from petsc4py.PETSc cimport SNES, PetscSNES

from petsc4py.PETSc import Error

cdef extern from "CavityFlow2Dimpl.h":
    ctypedef struct Params:
        double alpha_, lidvelocity_, prandtl_, grashof_
    int FormInitGuess(PetscDM da, PetscVec x, Params *p)
    int FormFunction (PetscDM da, PetscVec x, PetscVec F, Params *p)

def formInitGuess(Vec x, DA da, double alpha_, lidvelocity_, prandtl_, grashof_):
    cdef int ierr
    cdef Params p = {"alpha_" : alpha_, "lidvelocity_" : lidvelocity_,
                     "prandtl_" : prandtl_, "grashof_" : grashof_}
    ierr = FormInitGuess(da.dm, x.vec, &p)
    if ierr != 0: raise Error(ierr)

def formFunction(SNES snes, Vec x, Vec f, DA da, double alpha_, lidvelocity_, prandtl_, grashof_):
    cdef int ierr
    cdef Params p = {"alpha_" : alpha_, "lidvelocity_" : lidvelocity_,
                     "prandtl_" : prandtl_, "grashof_" : grashof_}

    ierr = FormFunction(da.dm, x.vec, f.vec, &p)
    if ierr != 0: raise Error(ierr)
