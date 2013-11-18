#include "Python.h"

static PyObject* hand_fib(PyObject *self, PyObject *args) 
{
    int n, a, b, i, tmp;
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
    a = 0; b = 1;
    for (i=0; i<n; i++) {
        tmp=a; a+=b; b=tmp;
    }
    return Py_BuildValue("i", a);
}

static PyMethodDef ExampleMethods[] = {
    {"fib",  hand_fib, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
inithand_fib(void)
{
    (void) Py_InitModule("hand_fib", ExampleMethods);
}
