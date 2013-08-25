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
<img src="/figures/intro/frequency_plot.png" style="width: 600px;"/>




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

<img src="/figures/intro/frequency_plot.png" style="width: 600px;"/>
