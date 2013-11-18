def fib(int n):
    cdef int a, b, i
    a, b = 0, 1
    for i in range(n):
        a, b = a+b, a
    return a
