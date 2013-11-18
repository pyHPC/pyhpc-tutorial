from timeit import timeit # for timing comparison

def pyfib(n):
    ''' Fibonnaci sequence in pure Python.
    Here for comparison with the Cython version.
    '''
    a, b = 0, 1
    for i in range(n):
        a, b = a+b, a
    return a

if __name__ == '__main__':
    repeat = 10000
    cython_time = timeit('cyfib(100)', 'from fib import fib as cyfib', number=repeat) / float(repeat)
    python_time = timeit('pyfib(100)', 'from __main__ import pyfib', number=repeat) / float(repeat)
    print "Cython time (s): %.2g" % cython_time
    print "Python time (s): %.2g" % python_time
    print "Cython X speedup: %.2f" % (python_time / cython_time)
