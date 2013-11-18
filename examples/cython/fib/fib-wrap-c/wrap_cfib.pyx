cdef extern from "cfib.h":
    int _cfib "cfib"(int n)

def cfib(int n):
    return _cfib(n)
