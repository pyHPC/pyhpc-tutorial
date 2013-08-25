import sys, petsc4py
petsc4py.init(sys.argv)
from petsc4py import PETSc

# this user class is an application
# context for the nonlinear problem
# at hand; it contains some parametes
# and knows how to compute residuals

"""Nonlinear driven cavity in 2d

This problem is modeled by the partial differential equation system

- Lap(U) - Grad_y(Omega) = 0
- Lap(V) + Grad_x(Omega) = 0
- Lap(Omega) + Div([U*Omega,V*Omega]) - GR*Grad_x(T) = 0
- Lap(T) + PR*Div([U*T,V*T]) = 0

in the unit square, which is uniformly discretized in each of x and
y in this simple encoding.

No-slip, rigid-wall Dirichlet conditions are used for [U,V].
Dirichlet conditions are used for Omega, based on the definition of
vorticity: Omega = - Grad_y(U) + Grad_x(V), where along each
constant coordinate boundary, the tangential derivative is zero.
Dirichlet conditions are used for T on the left and right walls,
and insulation homogeneous Neumann conditions are used for T on
the top and bottom walls. 

A finite difference approximation with the usual 5-point stencil 
is used to discretize the boundary value problem to obtain a 
nonlinear system of equations.  Upwinding is used for the divergence
(convective) terms and central for the gradient (source) terms.

The Jacobian can be either
* formed via finite differencing using coloring (the default), or
* applied matrix-free via the option -snes_mf 
(for larger grid problems this variant may not converge 
without a preconditioner due to ill-conditioning).

The 2D driven cavity problem is solved in a velocity-vorticity formulation.
The flow can be driven with the lid or with bouyancy or both:
-lidvelocity <lid>, where <lid> = dimensionless velocity of lid
-grashof <gr>, where <gr> = dimensionless temperature gradent
-prandtl <pr>, where <pr> = dimensionless thermal/momentum diffusity ratio
-contours : draw contour plots of solution
"""

import CavityFlow2D

nx = OptDB.getInt('nx', 32)
ny = OptDB.getInt('ny', nx)
alpha = OptDB.getReal('alpha', 6.8)
lidvelocity = OptDB.getReal('lidvelocity', 1.0/(nx*ny))
prandtl = OptDB.getReal('prandtl', 1.0)
grashof = OptDB.getReal('grashof', 1.0)

# create application context
# and PETSc nonlinear solver
snes = PETSc.SNES().create()
da = PETSc.DMDA().create([nx,ny],dof=4)

# set up solution vector
F = da.createGlobalVec()
snes.setFunction(CavityFlow2D.formFunction, F,
                 args=(da, alpha, lidvelocity, prandtl, grashof))

X = da.createGlobalVec()
CavityFlow2D.formInitGuess(X, da, grashof)

snes.setDM(da)
snes.setFromOptions()

# solve the nonlinear problem
snes.solve(None, x)

if OptDB.getBool('plot', True):
    da = PETSc.DA().create([nx,ny])
    u = da.createGlobalVec()
    x.copy(u)
    draw = PETSc.Viewer.DRAW()
    OptDB['draw_pause'] = 1
    draw(u)

if OptDB.getBool('plot_mpl', False):
    try:
        from matplotlib import pylab
    except ImportError:
        PETSc.Sys.Print("matplotlib not available")
    else:
        from numpy import mgrid
        X, Y =  mgrid[0:1:1j*nx,0:1:1j*ny]
        Z = x[...].reshape(nx,ny)
        pylab.figure()
        pylab.contourf(X,Y,Z)
        pylab.colorbar()
        pylab.plot(X.ravel(),Y.ravel(),'.k')
        pylab.axis('equal')
        pylab.show()
