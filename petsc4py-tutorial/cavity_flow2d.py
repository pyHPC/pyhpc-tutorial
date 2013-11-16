import argparse
import sys
import petsc4py
from numpy import mgrid
petsc4py.init(sys.argv)
from petsc4py import PETSc
try:
    from matplotlib import pyplot as plt
except ImportError:
    PETSc.Sys.Print("matplotlib not available")
    plt = None
import CavityFlow2D

"""
This problem is an adaptation of petsc example snes/ex19.c

    This problem is modeled by the partial differential equation system

\begin{eqnarray}
        - \triangle U - \nabla_y \Omega & = & 0  \\
        - \triangle V + \nabla_x\Omega & = & 0  \\
        - \triangle \Omega + \nabla \cdot ([U*\Omega,V*\Omega]) - GR* \nabla_x T & = & 0  \\
        - \triangle T + PR* \nabla \cdot ([U*T,V*T]) & = & 0
\end{eqnarray}

    in the unit square, which is uniformly discretized in each of x and y in this simple encoding.

    No-slip, rigid-wall Dirichlet conditions are used for $ [U,V]$.
    Dirichlet conditions are used for Omega, based on the definition of
    vorticity: $ \Omega = - \nabla_y U + \nabla_x V$, where along each
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

  ------------------------------------------------------------------------*/

The 2D driven cavity problem is solved in a velocity-vorticity formulation.
The flow can be driven with the lid or with bouyancy or with both.
"""


def get_args():
    OptDB = PETSc.Options()
    ignore = OptDB.getBool('--help', False)
    parser = argparse.ArgumentParser(description='2D Driven Cavity Flow',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--nx', default=32,help='number of grid points in x')
    parser.add_argument('--ny', default=32,help='number of grid points in y')
    parser.add_argument('--lidvelocity', help='dimensionless velocity of the lid\n(1/(nx*ny) if unspecified', type=float)
    parser.add_argument('--grashof', default=1.0,help='dimensionless temperature gradient', type=float)
    parser.add_argument('--prandtl', default=1.0,help='dimensionless thermal/momentum diffusivity ratio', type=float)
    parser.add_argument('--plot', help='use matplotlib to visualize solution')
    args, petsc_opts = parser.parse_known_args()

    if args.lidvelocity is None:
        args.lidvelocity = 1./(args.nx*args.ny)
    return args

def cavity_flow2D(nx, ny, lidvelocity, grashof, prandtl):
    # create application context
    # and PETSc nonlinear solver
    snes = PETSc.SNES().create()
    da = PETSc.DMDA().create([nx,ny],dof=4, stencil_width=1, stencil_type='star')

    # set up solution vector
    F = da.createGlobalVec()
    snes.setFunction(CavityFlow2D.formFunction, F,
                     args=(da, lidvelocity, prandtl, grashof))

    x = da.createGlobalVec()
    CavityFlow2D.formInitGuess(x, da, lidvelocity, prandtl, grashof)

    snes.setDM(da)
    snes.setFromOptions()

    # solve the nonlinear problem
    snes.solve(None, x)
    return x

def plot(x, nx, ny):
    """Plot solution to screen"""
    plt.ioff()
    Z = x[...].reshape(nx,ny,4)
    fig, axs = plt.subplots(2,2, figsize=(10,8))
    titles = ['u', 'v', 'vorticity', 'temperature']
    for idx, ax in enumerate(axs.ravel()):
        cs = ax.contourf(Z[:,:,idx], 100)
        fig.colorbar(cs, ax=ax, shrink=0.9)
        ax.set_title(titles[idx])
    plt.show()
        
if __name__ == "__main__":
    args = get_args()
    print "running cavity flow with: %s" % args
    x = cavity_flow2D(args.nx, args.ny, args.lidvelocity, args.grashof, args.prandtl)
    plot(x, args.nx, args.ny)                        
