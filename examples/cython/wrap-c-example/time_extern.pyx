'''
=============================================================================
time_extern extension module.  Simple wrapper that calls into the localtime()
and time() functions in the C standard library.

Methods:
--------

	get_date() -- returns a tuple with the current day, month and year.
=============================================================================
'''


cdef extern from "time.h":

    struct tm:
        int tm_mday
        int tm_mon
        int tm_year

    ctypedef long time_t
    tm* localtime(time_t *timer)
    time_t time(time_t *tloc)

def get_date():
    """Return a tuple with the current day, month and year.
    """
    cdef:
        time_t t
        tm* ts

    t = time(NULL)
    ts = localtime(&t)
    return ts.tm_mday, ts.tm_mon + 1, ts.tm_year + 1900

