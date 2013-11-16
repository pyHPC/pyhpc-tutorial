#ifndef CAVITYFLOW2D_H
#define CAVITYFLOW2D_H

#include <petsc.h>

#if PETSC_VERSION_(3,1,0)
#include <petscvec.h>
#include <petscmat.h>
#include <petscda.h>
#endif

typedef struct Params {
  double lidvelocity_, prandtl_, grashof_;
} Params;

typedef struct {
  PetscScalar u,v,omega,temp;
} Field;

PetscErrorCode FormInitGuess(DM da, Vec x, Params *p);
PetscErrorCode FormFunction(DM da, Vec x, Vec F, Params *p);
PetscErrorCode FormFunctionLocal(DMDALocalInfo *info,Field **x,Field **f,Params *p);

#endif /* !CAVITYFLOW2D_H */
