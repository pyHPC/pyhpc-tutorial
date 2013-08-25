import pylab

n, bins, patches = pylab.hist(pylab.randn(1000), 40, normed=1)
l, = pylab.plot(bins, pylab.normpdf(bins, 0.0, 1.0), 'r--', label='fit', linewidth=3)
pylab.legend([l, patches[0]], ['fit', 'hist'])

pylab.show()
