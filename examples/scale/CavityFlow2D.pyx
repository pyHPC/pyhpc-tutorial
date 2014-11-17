from petsc4py.PETSc cimport Vec,  PetscVec
from petsc4py.PETSc cimport DM,   PetscDM
from petsc4py.PETSc cimport SNES, PetscSNES

from petsc4py.PETSc import Error

cdef extern from "CavityFlow2Dimpl.h":
    ctypedef struct Params:
        double lidvelocity_, prandtl_, grashof_
    int FormInitGuess(PetscDM da, PetscVec x, Params *p)
    int FormFunction (PetscDM da, PetscVec x, PetscVec F, Params *p)

def formInitGuess(Vec x, DM da, double lidvelocity_, double prandtl_, double grashof_):
    cdef int ierr
    cdef Params p = {"lidvelocity_" : lidvelocity_, "prandtl_" : prandtl_, "grashof_" : grashof_}
    ierr = FormInitGuess(da.dm, x.vec, &p)
    if ierr != 0: raise Error(ierr)

def formFunction(SNES snes, Vec x, Vec f, DM da, double lidvelocity_, double prandtl_, double grashof_):
    cdef int ierr
    cdef Params p = {"lidvelocity_" : lidvelocity_, "prandtl_" : prandtl_, "grashof_" : grashof_}

    ierr = FormFunction(da.dm, x.vec, f.vec, &p)
    if ierr != 0: raise Error(ierr)
