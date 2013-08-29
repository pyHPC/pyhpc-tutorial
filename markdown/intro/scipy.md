Scipy : high-level scientific computing
---------------------------------------

Set of useful modules for all parts of scientific computing.

<ul>
<li class="left">cluster</li>
<li class="left">constants </li>
<li class="left">fftpack </li>  
<li class="left">integrate </li>
<li class="left">interpolate </li>
<li class="left">io </li>
<li class="left">linalg </li>
<li class="left">ndimage </li>
<li class="right">odr </li>
<li class="right">optimize </li>
<li class="right">signal </li>
<li class="right">sparse </li>
<li class="right">spatial </li>
<li class="right">special </li>
<li class="right">stats </li>
</ul>



### Import

In general, you can grab SciPy functionality via

```python
  import scipy 
```



### SciPy Constants

A plethora of important, fundamental constants can be found in
**scipy.constants**. NOTE: However, this module is not automatically
included when you **import scipy**. Still, some very basic pieces of
information are given as module attributes.




The following, for example:

```python
  import scipy.constants 
  import math
  
  print("SciPy thinks that pi = %.16f"%scipy.constants.pi) 
  print("While math thinks that pi = %.16f"%math.pi) 
  print("SciPy also thinks that the speed of light is c = %.1F"%scipy.constants.c) 
```

will return

```python
  >>> SciPy thinks that pi = 3.1415926535897931 
  >>> While math thinks that pi = 3.1415926535897931 
  >>> SciPy also thinks that the speed of light is c = 299792458.0 
```




However, the real value of SciPy Constants is its enormous physical
constant database. These are of the form:
**scipy.constants.physical\_constants[name] = (value, units,
uncertainty)**.

For example, the mass of an alpha particle is:

```python

  >>> scipy.constants.physical_constants["alpha particle mass"] 
  >>> (6.6446564999999997e-27, 'kg', 1.1e-33) 
```



How can you tell what the key is for this function? My favorite way is
with the scipy.constants.find() method.

```python
  scipy.constants.find("light")
```

gives :

```python
  ['speed of light in vacuum']
```



But buyer beware! Let's look at the speed of light again.

```python
  >>> print("c = %s"%str(scipy.constants.physical_constants["speed of light in vacuum"]))
  >>> c = (299792458.0, 'm s^-1', 0.0)
```



The uncertainty in c should not be zero! Right? Wrong. The
[meter](http://en.wikipedia.org/wiki/Metre) is in fact set by the speed of light
in a vacuum. So there is, by definition, no error. However, this has not always
been the case.  Moreover, any actual determination of the **c** or the meter has
a measurement uncertainty, but SciPy does not acknowledge it.




**BASIC LESSON:** As always, pay attention.

Check http://docs.scipy.org/doc/scipy/reference/constants.html for a complete
constants listing.

The above code is reproduced concisely in the constants.py file found in
the SciPy directory of your PyTrieste repository.




### SciPy Special Functions


Code that numerically approximates common (and some not-so-common)
special functions can be found in **scipy.special**. Here you can find
things like error functions, gamma functions, Legendre polynomials, etc.
But as a example let's focus on my favorites: the Bessel functions.




```python
  from scipy.special import * 
  from pylab import *
  
  x = arange(0.0, 10.1, 0.1)
  
  for n in range(4): 
    j = jn(n, x) 
    plot(x, j, 'k-') 
    text(x[10*(n+1)+1], j[10*(n+1)], r'$J_%r$'%n)
  
  for n in range(3): 
    y = yn(n, x) plot(x, y, 'k--') 
    text(x[10*(n)+6], y[10*(n)+5], r'$Y_%r$'%n)
  
  axis([0, 10, -2, 1.25]) 
  xlabel(r'$x$') 
  ylabel("Bessel Functions")
  
  show() 
```




These 20-ish lines of code should produce :

![](../figures/intro/BesselFigure.png)




Note that the figure that was created here is a reproduction of Figure
6.5.1 in ''Numerical Recipes'' by W. H. Press, et al...
(http://www.nr.com/).

Check out http://docs.scipy.org/doc/scipy/reference/special.html for a complete
listing of special functions.




### SciPy Integration



Tools used to calculate numerical, definite integrals may be found in
the **integrate** module. There are two basic ways you can integrate in
SciPy:

1.  Integrate a function,
2.  Integrate piecewise data.

First, let's deal with integration of functions. Recall that in Python,
functions are also objects. Therefore you can pass functions as
arguments to other functions! Just make sure that the function that you
want to integrate returns a float, or at the very least, an object that
has a **__float__()** method.




### Integration Example: 1D


The simplest way to compute a functions definite integral is via the
**quad(...)** function. The script

```python
  import scipy.integrate #For kicks, let's also grab
  import scipy.special
  import numpy
  def CrazyFunc(x):
    return (scipy.special.i1(x) - 1)**3

  print("Try integrating CrazyFunc on the range [-5, 10]...")
  
  val, err = scipy.integrate.quad(CrazyFunc, -5, 10)

  print("A Crazy Function integrates to %.8E"%val)
  print("And with insanely low error of %.8E"%err)
```

will return


```python
  >>> Try integrating CrazyFunc on the range [-5, 10]...  
  >>> A Crazy Function integrates to 6.65625226E+09 
  >>> And with insanely low error of 3.21172897E-03
```




### Integration Example: Infinite Limits


You can also use **scipy.integrate.Inf** for infinity in the limits of
integration. For example, try integrating e\^x on `[-inf, 0]`:

```python
  >>> print("(val, err) = " + 
      str( scipy.integrate.quad(scipy.exp, -scipy.integrate.Inf, 0.0) ))
```

will return :

```python
  >>> (val, err) = (1.0000000000000002, 5.8426067429060041e-11)
```



### Integration Example: 2D

Two dimensional integrations follow similarly to the 1D case. However,
now we need to use the **dblquad( f(y,x), ...)** function instead of
simply **quad( f(x), ...)**. Because a picture is worth 10\^3 words,
SciPy computes the right-hand side of the following equation:

![](../figures/intro/dblquad.png)

More information on the justification of this integral may be found at
http://en.wikipedia.org/wiki/Order\_of\_integration\_(calculus). For
example, let's try to integrate the surface area of a unit sphere:




```python
  def dA_Sphere(phi, theta):
    return  scipy.sin(phi)

  print("Integrate the surface area of the unit sphere...")
  val, err = scipy.integrate.dblquad(dA_Sphere, 0.0, 2.0*scipy.pi, 
    lambda theta: 0.0, 
    lambda theta: scipy.pi )
  print("val = %.8F"%val)
  print("err = %.8E"%err)
```

This will return :

```python
  >>> Integrate the surface area of the unit sphere...  
  >>> val = 12.56637061
  >>> err = 1.39514740E-13
```




There are a couple of subtleties here. First is that the function you
are integrating over is defined as **f(y,x)** and NOT the more standard
**f(x,y)**. Moreover, while **x**'s limits of integration are given
directly **[0, 2*pi]**,**y**'s limits have to be functions**[g(x),
h(x)]*\* (given by the 'lambdas' here). This method of doing double
integrals allows for**y*\* to have a more complicated edge in**x*\* than
a simple point. This is great for some functions but a little annoying
for simple integrations. In any event, the above integral computes the
surface are of a unit sphere to be **4*pi*\* to within floating point
error.




### Integration Example: 3D


Three dimensional integration is more similar to 2D than 1D. Once again,
we define our function variables in reverse order, **f(z, y, x)**, and
integrate using **tplquad( f(z, y, x) )**. Moreover, **z** has limits of
integration defined by surfaces give as functions **[q(x,y), r(x,y)]**.
Thus, **tplquad(...)** integrates the right-hand side of :

![](../figures/intro/trplquad.png)

To continue with the previous example, let's try integrating the volume
of a sphere. Take the radius here to be 3.5.




```python
  def dV_Sphere(phi, theta, r):
    return r * r * dA_Sphere(phi, theta)

  print("Integrate the volume of a sphere with r=3.5...")
  val, err = scipy.integrate.tplquad(dV_Sphere, 0.0, 3.5, lambda r: 0.0,
    lambda r: 2.0*scipy.pi, lambda x, y: 0.0, lambda x, y: scipy.pi)
  print("val = %.8F"%val)
  print("err = %.8E"%err)
```

will return:

```python
  >>> Integrate the volume of a sphere with r=3.5...
  >>> val = 179.59438003
  >>> err = 1.99389816E-12
```

A simple hand calculation verifies this result.




### Integration Example: Trapazoidal


Now, only very rarely will scientists (and even more rarely engineers)
will truely 'know' the function that they wish to integrate. Much more
often we'll have piecewise data that we wish numerically integrate (ie
sum an array y(x), biased by array x). This can be done in SciPy through
the **trapz(...)** function.




```python
  y = range(0, 11)
  print("Trapazoidally integrate y = x on [0,10]...")
  val = scipy.integrate.trapz(y)
  print("val = %F"%val)
```

will return:

```python
  >>> Trapazoidally integrate y = x on [0,10]...
  >>> val = 50.000000
```

The above takes a series of y-values that are implicitly spaced 1-unit
apart in x and 'trapazoidally integrates' them. Basically, just a sum.



However, you can use the **x= [0, 3,...]** or **dx = 3** argument
keywords to explicitly declare different spacings in x. For example,
with y = x\^2:

```python
  x = numpy.arange(0.0, 20.5, 0.5)
  y = x * x
  print("Trapazoidally integrate y = x^2 on [0,20] with half steps...")
  val = scipy.integrate.trapz(y, x)
  print("val = %F"%val)
```

```python
  >>> Trapazoidally integrate y = x^2 on [0,20] with half steps...
  >>> val = 2667.500000
```

```python
  print("Trapazoidally integrate y = x^2 with dx = 0.5...")
  val = scipy.integrate.trapz(y, dx = 0.5)
  print("val = %F"%val)
```

```python
  >>> Trapazoidally integrate y = x^2 with dx = 0.5...
  >>> val = 2667.500000
```




### Integration Example: Ordinary Differential Equations


Say that you have an ODE of the form **dy/dt = f(y, t)** that you
''really'' need integrated. Then you, my friend, are in luck! SciPy can
do this for you using the **scipy.integrate.odeint** function. This is
of the form:

```python
  odeint( f, y0, [t0, t1, ...])
```

For example take the decay equation:
   (y, t) = - lambda * y 

We can then try integrating this using a decay constant of 0.2`:

```python
  def dDecay(y, t, lam):
    return -lam*y

  vals = scipy.integrate.odeint( lambda y, t: dDecay(y, t, 0.2), 1.0, [0.0, 10.0] )
  print("If you start with a mass of y(0) = %F"%vals[0][0])
  print("you'll only have y(t= 10) = %F left."%vals[1][0])
```



This will return

```python
  >>> If you start with a mass of y(0) = 1.000000
  >>> you'll only have y(t= 10) = 0.135335 left.
```

Check out http://docs.scipy.org/doc/scipy/reference/integrate.html for more
information on integreation.



## SciPy Image Tricks

#### SciPy has the ability to treat 2D & 3D arrays as images. 

- convert PIL images
- read in external files as numpy arrays! 
- buried within the ```miscellaneous``` module.




[http://en.wikipedia.org/wiki/File:JumpingRabbit.JPG](http://en.wikipedia.org/wiki/File:JumpingRabbit.JPG)

![](../figures/intro/image.jpg)




```python
  import scipy.misc
  img = scipy.misc.imread("image.jpg")
  #Note that this really is an array!
  print(str(img))
```




```python

  >>> [[[130 174  27]
  >>>   [129 173  24]
  >>>   [127 171  22]
  >>>   ..., 
  >>>   [147 192  41]
  >>>   [146 190  41]
  >>>   [146 190  41]]
  >>> 
  >>>  [[137 177  29]
  
  >>>   [133 175  27]
  >>>   [130 173  21]
  >>>   ..., 
  >>>   [147 192  37]
  >>>   [149 194  41]
  >>>   [149 194  41]]
  >>> 
  >>>  [[141 177  29]
  >>>   [137 176  25]
  >>>   [130 174  19]
  >>>   ..., 
  >>>   [148 194  34]
  >>>   [149 195  35]
  >>>   [149 195  35]]
  >>> 
  >>>  ..., 
  >>>  [[ 77 126   1]
  >>>   [ 87 137  14]
  >>>   [ 85 139   0]
  >>>   ..., 
  >>>   [ 77 128   0]
  >>>   [ 99 159   3]
  >>>   [128 183  17]]
  
  >>>  [[ 86 139   0]
  >>>   [ 90 141  12]
  >>>   [ 82 136   0]
  >>>   ..., 
  >>>   [ 66 114   2]
  >>>   [102 160   0]
  >>>   [119 174  11]]
  >>> 
  >>>  [[ 89 140   0]
  >>>   [ 79 129   8]
  >>>   [ 87 139   2]
  >>>   ..., 
  >>>   [ 67 117   4]
  >>>   [ 81 138   0]
  >>>   [117 172  18]]]
```




We can now apply some basic filters...

```python
  img = scipy.misc.imfilter(img, 'blur')
```

We can even rotate the image, counter-clockwise by degrees.

```python
  img = scipy.misc.imrotate(img, 45)
```

And then, we can rewrite the array to an image file.

```python
  scipy.misc.imsave("image1.jpg", img)
```




These functions produce the following image:

![](../figures/intro/image1.jpg)




Because the array takes integer values from 0 - 255, we can easily
define our own filters as well! For instance, you could write a two-line
function to inverse the image...

```python
  def InverseImage(imgarr):
     return 255 - imgarr
  #Starting fresh we get...
  img = scipy.misc.imread("image.jpg")
  img = scipy.misc.imrotate(img, 330)
  img = InverseImage(img)
  scipy.misc.imsave("image2.jpg", img)
```




Having this much fun, the rabbit becomes a twisted shade of its former
self!

![](../figures/intro/image2.jpg)


Check out http://docs.scipy.org/doc/scipy/reference/misc.html for a complete
listing of associated image functions.



### File input/output:

Loading and saving matlab files::

```python
    >>> from scipy import io as spio
    >>> a = np.ones((3, 3))
    >>> spio.savemat('file.mat', {'a': a}) # savemat expects a dictionary
    >>> data = spio.loadmat('file.mat', struct_as_record=True)
    >>> data['a']
    array([[ 1.,  1.,  1.],
           [ 1.,  1.,  1.],
           [ 1.,  1.,  1.]])
```



Reading images::

```python
    >>> from scipy import misc
    >>> misc.imread('fname.png')
    >>> # Matplotlib also has a similar function
    >>> import matplotlib.pyplot as plt
    >>> plt.imread('fname.png')
```



See also:

    * Load text files: :func:`numpy.loadtxt`/:func:`numpy.savetxt`

    * Clever loading of text/csv files:
      :func:`numpy.genfromtxt`/:func:`numpy.recfromcsv`

    * Fast and efficient, but numpy-specific, binary format:
      :func:`numpy.save`/:func:`numpy.load`



### Special functions:

 * Bessel function, such as :func:`scipy.special.jn` (nth integer order Bessel
   function)

 * Elliptic function (`scipy.special.ellipj` for the Jacobian elliptic
   function, ...)

 * Gamma function: `scipy.special.gamma`, also note
   `scipy.special.gammaln` which
   will give the log of Gamma to a higher numerical precision.

 * Erf, the area under a Gaussian curve: `scipy.special.erf`




### Linear algebra operations:

The `scipy.linalg` module provides standard linear algebra
operations, relying on an underlying efficient implementation (BLAS,
LAPACK).




* The `scipy.linalg.det` function computes the determinant of a
  square matrix::

```python
    >>> from scipy import linalg
    >>> arr = np.array([[1, 2],
    ...                 [3, 4]])
    >>> linalg.det(arr)
    -2.0
    >>> arr = np.array([[3, 2],
    ...                 [6, 4]])
    >>> linalg.det(arr)
    0.0
    >>> linalg.det(np.ones((3, 4)))
    Traceback (most recent call last):
    ...
    ValueError: expected square matrix
```



* The `scipy.linalg.inv` function computes the inverse of a square
  matrix::

```python
    >>> arr = np.array([[1, 2],
    ...                 [3, 4]])
    >>> iarr = linalg.inv(arr)
    >>> iarr
    array([[-2. ,  1. ],
           [ 1.5, -0.5]])
    >>> np.allclose(np.dot(arr, iarr), np.eye(2))
    True
```




Finally computing the inverse of a singular matrix (its determinant is zero)
  will raise ``LinAlgError``::

```python
>>> arr = np.array([[3, 2],
...                 [6, 4]])
>>> linalg.inv(arr)
Traceback (most recent call last):
...
LinAlgError: singular matrix
```



* More advanced operations are available, for example singular-value
  decomposition (SVD)::

```python
    >>> arr = np.arange(9).reshape((3, 3)) + np.diag([1, 0, 1])
    >>> uarr, spec, vharr = linalg.svd(arr)
```

  The resulting array spectrum is::

```python
    >>> spec
    array([ 14.88982544,   0.45294236,   0.29654967])
```

  The original matrix can be re-composed by matrix multiplication of the outputs of
  ``svd`` with ``np.dot``::

```python
    >>> sarr = np.diag(spec)
    >>> svd_mat = uarr.dot(sarr).dot(vharr)
    >>> np.allclose(svd_mat, arr)
    True
```




### Fast Fourier transforms:


The `scipy.fftpack` module allows to compute fast Fourier transforms.
As an illustration, a (noisy) input signal may look like::
```python
    >>> time_step = 0.02
    >>> period = 5.
    >>> time_vec = np.arange(0, 20, time_step)
    >>> sig = np.sin(2 * np.pi / period * time_vec) + \
    ...       0.5 * np.random.randn(time_vec.size)
```



The observer doesn't know the signal frequency, only
the sampling time step of the signal ``sig``. The signal
is supposed to come from a real function so the Fourier transform
will be symmetric.
<br/><br/>
The `scipy.fftpack.fftfreq` function will generate the sampling frequencies and
`scipy.fftpack.fft` will compute the fast Fourier transform::

```python
    >>> from scipy import fftpack
    >>> sample_freq = fftpack.fftfreq(sig.size, d=time_step)
    >>> sig_fft = fftpack.fft(sig)
```



Because the resulting power is symmetric, only the positive part of the
spectrum needs to be used for finding the frequency::

```python
    >>> pidxs = np.where(sample_freq > 0)
    >>> freqs = sample_freq[pidxs]
    >>> power = np.abs(sig_fft)[pidxs]
```



The signal frequency can be found by::

```python
    >>> freq = freqs[power.argmax()]
    >>> np.allclose(freq, 1./period)  # check that correct freq is found
    True
```
<img src="../figures/intro/frequency_plot.png" style="width: 600px;"/>




Now the high-frequency noise will be removed from the Fourier transformed
signal::

```python
    >>> sig_fft[np.abs(sample_freq) > freq] = 0
```

The resulting filtered signal can be computed by the
`scipy.fftpack.ifft` function::

```python
    >>> main_sig = fftpack.ifft(sig_fft)
```



The result can be viewed with::

```python
    >>> import pylab as plt
    >>> plt.figure()
    >>> plt.plot(time_vec, sig)
    >>> plt.plot(time_vec, main_sig, linewidth=3)
    >>> plt.xlabel('Time [s]')
    >>> plt.ylabel('Amplitude')
```

<img src="../figures/intro/frequency_plot.png" style="width: 600px;"/>
