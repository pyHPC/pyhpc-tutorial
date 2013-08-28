# Introduction to petsc4py

## Overview
* petsc4py is a Pythonic interface to PETSc (pronounced: "pet-see"), the
Portable Extensible Toolkit for Scientific Computing.  

* PETSc is a suite
of data structures and routines for the scalable (parallel) solution of
scientific applications modeled by partial differential equations. 
<details>
PETSc employs a single program multiple (distributed) data programming
paradigm, and MPI for all message-passing communication.
PETSc is intended for use in large-scale application projects, and
several ongoing computational science projects are built around the
PETSc libraries. With strict attention to component interoperability,
PETSc facilitates the integration of independently developed application
modules, which often most naturally employ different coding styles and
data structures.
</details>

* PETSc and petsc4py have been designed to be as easy as possible to use
for beginners while still delivering the performance expected of high
performance numerical codes. 
<details> 
Moreover, PETSc's careful design allows advanced users to have detailed
control over the solution process.  PETSc includes an expanding suite of
parallel linear and nonlinear equation solvers that are easily used in
application codes written in C, C++, and Fortran. PETSc provides many of
the mechanisms needed within parallel application codes, such as simple
parallel matrix and vector assembly routines that allow the overlap of
communication and computation.
</details>

## Outline
 * Dive into petsc4py - Solving the Poisson Equation in 3 Dimensions
    * Vec - distributed vectors
    * Mat - distributed matrices and matrix operators
    * KSP - Krylov subspace methods
    * PC - preconditioners and direct solvers
 * More on PETSc objects
    * DM - distributed meshes
    * DMDA - structured distributed meshes
    * SNES - Newton-like methods for nonlinear systems
     * TS - time integrators and pseudo-transient continuation methods
 * Putting it all together - Steady thermal and lid-driven cavity flow

# Dive into petsc4py

## Laplace's and Poisson's Equations

<details>The Laplacian operator appears in partial differential equations that
describe many of the conservation laws of continuum mechanics,
electrodynamics, and many other systems.  In its simplest form,
Laplace's equation, the operator appears as a homogeneous potential
equation: </details>

$$-\nabla^2u = 0$$

Note the usage of the minus in our definition, allowing us to deal with
the Laplacian as a positive definite operator.

The inhomogenous potential equation with sources is well known as
Poisson's equation:

$$-\nabla^2u = f$$

## Discretization of Poisson's Equation

For this exercise, we select the second-order finite difference
approximation to the solution, source, and Laplace operator: 

$$\mathtt{x} \approx u, \ \ \ \mathtt{b} \approx f, \ \ \ \mathtt{A} \approx \nabla^2u$$

We would now like to solve the following system of linear equations:
$$\mathtt{A}\mathtt{x} = \mathtt{b}$$

<details>
We represent `x` and `b` as PETSc `Vec` objects in the code.  We
represent `A` as a `Mat` object.
</details>

## The PETSc Mat object

* The PETSc `Mat` object is a generic discrete
  linear operator.
  
* Layout is compressed row storage (Yale) by default

* (Parallel) rows are distributed across processors 

* To every extent possible, `Mat` abstracts the *matrix data
  layout* from the code

## Construction of a Python shell Mat object

<details>For several interesting iterative numerical solvers, we do not need to
store `A` directly, and we would instead like to define functions that
mimic several aspects of the operator, such as matrix-vector
multiplication.  In PETSc, this concept is called a `shell`, and by the
dynamic polymorphism of the `Mat` object, we can compose a `shell Mat`
at runtime.  We'll look more into the details of how `A` is implemented later, but
for now PETSc thinks of it as our linear operator, and so should we!</details>

```{.python}
# number of nodes in each direction
# excluding those at the boundary
n = 32
# grid spacing
h = 1.0/(n+1) 
A = PETSc.Mat().create()
A.setSizes([n**3, n**3])
A.setType('python')
shell = Del2Mat(n) # shell context
A.setPythonContext(shell)
A.setUp()
```

## The PETSc Vec object

* The PETSc `Vec` object is a generic
  element of a discrete vector space.
  
* Scalar elements of the vector are distributed across processors in the
  same manner that `Mat` rows are

* Supports many common mathematical operations in conjunction with the
  `Mat` object
  
* To every extent possible, `Vec` abstracts the *parallel array layout* from the
  code

## Setting up solution and source Vecs

<details>We could create our `x` and `b` `Vecs` independently of `A`, but since
it has already been constructed, we can use its `getVecs` method to
build them for us. *In the past, the PETSc developers were a little
sloppy with the choice of verbs such as "get, create, set, and replace",
getVecs should probably have been createVecs, and may get renamed to
this in a future version.*

1 is a pretty boring choice of right-hand sides, we'll spice this up a
little later.</details>

```{.python}
x, b = A.getVecs()
# set the initial guess to 0
x.set(0.0)
# set the right-hand side to 1
b.set(1.0)
```

## The PETSc KSP object

* The PETSc `KSP` object is a generic solution
  strategy for a system of linear equations
  
* The `KSP` object supports serial and parallel, iterative and direct
  linear solvers

* The name comes from Krylov Subspace, which refers to the collection of
  vectors spanned by the space: $[b Ab A^2b ... A^nb]$, and which is the
  basis for many iterative methods
  
* To every extent possible,`KSP` abstracts the *solver
  strategy* from the code

## Setting up the Krylov solver (KSP)
<details>
Our next step is to choose a solution scheme for solving the system of
linear equations.  If we don't set a type by default, PETSc will utilize
the GMRES method, but since we know our system is symmetric, we select
the Conjugate Gradients algorithm, `cg`, for better performance. </details>

```{.python}
ksp = PETSc.KSP().create()
ksp.setType('cg')
```

<details>Since we have a `shell Mat`, most of the interesting preconditioners
that rely on access to the `Mat` data structure won't work, so we turn
preconditioning off.</details>

```{.python}
pc = ksp.getPC()
pc.setType('none')
```

<details>
Finally, we inform the `KSP` object of the operator we are solving for
(we could set an additional preconditioning operator here if we liked),
then use the `setFromOptions` function, which allows us to override the
options set here from the command-line. </details>

```{.python}
ksp.setOperators(A)
ksp.setFromOptions()
ksp.solve(b, x)
```

## Some notes on the syntactic sugar in petsc4py and matplotlib

The `poisson3d.py` demo contains two examples of syntactic sugar that
should be noted:

<details>First, the function call to `numpy.mgrid` contains  complex step
lengths.  This is a somewhat dirty (but useful) overload for the `mgrid` function,
allowing the user to request $n$ equally spaced points inclusively
containing 0 and 1.</details>

```{.python}
        X, Y =  mgrid[0:1:1j*n,0:1:1j*n]
```

<details>In a similar vein, the ellipses object in the slice passed to
the `Vec` object, `[...]`, is syntactic sugar for `getArray()`, which
returns a `numpy` array representing the data owned by the local process.</details>

```{.python}
        Z = x[...].reshape(n,n,n)[:,:,n/2-2]
```

## Exercise and Demonstration

<details>
Notes from the demo:
* Launch serial jobs with `python script.py`
* Launch parallel jobs with `mpirun -n 4 python script.py`
* Use the `-h` flag after `script.py` to get help on specific PETSc options
</details>

## DM - distributed meshes

* The PETSc `DM` object is a generic geometric
  discretization of a physical space 
<details> 
More specifically, the `DM` object maps the entries in a `Vec` object
  to their geometric locations in 1, 2, and 3 dimensional space and
  coordinates the parallel distribution of this data  
</details>

* When a stencil extent has been set, the `DM` object can build
  and maintain `local` and `global` vectors  

      + `global` vectors perfectly decompose the spatial discretization 
      + `local` vectors contain "ghost" values, read-only values needed by
      each processor to compute on its local data

* The `DMDA` object, which implements `DM` for simple Cartesian
  discretizations, provides more intuition on how `DM` works

## DMDA - structured distributed meshes

* The PETSc `DMDA` object is a generic geometric
  discretization of a structured Cartesian physical space 
<details>
In the context of PETSc, a structured space has a fixed number of grid
  points in each direction, with either absorbing, reflective, or
  periodic boundary conditions.  This corresponds well to structured
  finite difference approximations as well as simple quadrilateral and
  tetrahedral finite element meshes. 
</details>

* The `DMDA` object can represent structured grids in 1, 2, or 3
  dimensions, and also provides convenient array pointers for computing
  on the boundaries and interior
  
* To every extent possible, the `DMDA` abstracts the *parallel data layout* from the code

## SNES - Newton-like methods for nonlinear systems

* The PETSc `SNES` object is a generic solution
  strategy for a nonlinear system of equations of the form:
  
  $$ F(x) = 0 $$
<details>

  The `SNES` object is usually built on top of a Newton or quasi-Newton
iteration, with search directions updated by solving the Jacobian
  using a `KSP` at each step
</details>
  
* In the simplest case, the user provides a structured domain and a routine for computing
  $F(x)$, and PETSc does the rest by approximating the Jacobian: `-snes_fd`
  
* `SNES` also supports matrix-free strategies: `-snes_mf`
  
* To every extent possible, `SNES` abstracts the *nonlinear solver
  strategy* from the code 

## TS - time integrators 

* The PETSc `TS` object is a generic solution
  strategy for ordinary differential equations and differential
  algebraic equations

* Provides Forward Euler, Backward Euler, and a variety of Runge-Kutta and Strong
  Stability Preserving time integrators
  
* Can be used to solve equations in steady-state via pseudo-timestepping

* To every extent possible, `TS` abstracts the *time-stepping
  strategy* from the code 

# Putting it all together - Steady thermal and lid-driven cavity flow


