from __future__ import print_function
from subprocess import check_call
import sys, platform

def compiler(setup_name):
    # the Python binary full path.
    exe = sys.executable

    # figure out what platform we're on and adjust the commandline flags accordingly.
    extras = []
    if platform.system() == 'Windows':
        extras = ['--compiler=mingw32']

    # The distutils command to execute
    cmd = [exe, setup_name, 'build_ext', '--inplace'] + extras
    print(cmd)

    # runs the command and raises an exception on failure.
    check_call(cmd)

def importer(module_name, function_name):

    # Remove any common ending, both for pure python and extension modules.
    for ending in ('.py', '.pyc', '.so', '.pyd'):
        module_name = module_name.rsplit(ending)[0]

    mod = __import__(module_name)

    # import the required function, re-raising an ImportError on failure.
    try:
        return getattr(mod, function_name)
    except AttributeError:
        raise ImportError("cannot import name %s" % function_name)
