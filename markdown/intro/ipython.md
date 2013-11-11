The interactive workflow: IPython and a text editor
---------------------------------------------------

- Not a single "blessed" environment
- IPython provides many interactive elements missing in base interpreter
    - tab completion
    - documentation in a pager
    - notebook interface for literate style
    - simple parallel features

<aside class="notes">
**Interactive work to test and understand algorithms:** In this section,
we describe an interactive workflow with [IPython](http://ipython.org)\_
that is handy to explore and understand algorithms.

Python is a general-purpose language. As such, there is not one blessed
environment to work in, and not only one way of using it. Although this
makes it harder for beginners to find their way, it makes it possible
for Python to be used to write programs, in web servers, or embedded
devices.
</aside>




### Command line interaction

Start `ipython`:

```bash
$ ipython
Python 2.7.5 (default, Aug  2 2013, 22:27:50) 
Type "copyright", "credits" or "license" for more information.

IPython 0.13.2 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: print("Hello World")
Hello World
```



### Getting help

Getting help by using the **?** operator after an object:


```
In [6]: list?
Type:       type
String Form:<type 'list'>
Namespace:  Python builtin
Docstring:
list() -> new empty list
list(iterable) -> new list initialized from iterable's items
```



View *python* source with **??** operator:
```python
In [13]: os.path.join??
Type:       function
String Form:<function join at 0x10198eed8>
File:       /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Versions/2.7/lib/python2.7/posixpath.py
Definition: os.path.join(a, *p)
Source:
def join(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded.  An empty last part will result in a path that
    ends with a separator."""
    path = a
    for b in p:
        if b.startswith('/'):
            path = b
        elif path == '' or path.endswith('/'):
            path +=  b
        else:
            path += '/' + b
    return path
```



### IPython Tips and Tricks

Ipython also contains many *magic* functions for iterating on your algorithm:

- `%run` - run file as if it were a script 
- `%timeit` - times a single expression
- `%debug` - debug the last traceback



`%run` - run file as if it were a script 

```python
In [14]: %run examples/intro/04_regular_expressions.py
Reading from examples/intro/../data/python.bib
Found a book with the tag 'Langtangen2011'
The title is 'A Primer on Scientific Programming with Python'
Found a book with the tag 'Langtangen2010'
The title is 'Python Scripting for Computational Science'
In [15]: infile
Out[15]: u'examples/intro/../data/python.bib'
```



`%timeit` - times a single expression

```python
In [16]: %timeit range(100)
1000000 loops, best of 3: 1.2 us per loop
In [17]: %timeit sum(xrange(100))
100000 loops, best of 3: 1.54 us per loop
In [18]: %timeit sum(range(100))
100000 loops, best of 3: 2.65 us per loop
In [19]: def loop_sum():
   ....:     sum = 0
   ....:     for i in xrange(100):
   ....:         sum += i
   ....:     return sum
   ....: 

In [20]: %timeit loop_sum()
100000 loops, best of 3: 6.72 us per loop
```



`%debug` - debug the last traceback

```
In [17]: %run examples/intro/05_debug.py
IndexError                                Traceback (most recent call last)
<snip>
In [18]: %debug
> /Users/aterrel/Dropbox/Documents/Teaching/pyhpc-tutorial/examples/intro/05_debug.py(3)<module>()
      1 l = range(10)
      2 
----> 3 l[10] = 5

ipdb> print(l)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ipdb> print(len(l))
10
ipdb> print(l[9])
9
```



Other useful magic functions are:

-   `%cd` to change the current directory (see `alias` for other mapped shell commands). 

-   `!<command>` to use shell commands.

-   `%cpaste` allows you to paste code, especially code from websites
    which has been prefixed with the standard python prompt (e.g. `>>>`)
    or with an ipython prompt, (e.g. `in [3]`):

-   `%history` to see your history (or save your session)

-   To explore use *tab completion* 

