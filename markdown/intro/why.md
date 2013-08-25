Why Python?
-----------

### The scientist's needs

-   Get data (simulation, experiment control)

-   Manipulate and process data.

-   Visualize results... to understand what we are doing!

-   Communicate results: produce figures for reports or publications,
    write presentations.



### Specifications

-   Existing **bricks** corresponding to classical numerical methods or basic actions

-   Easy to learn

-   Easy to communicate with collaborators, students, customers, to make
    the code live within a lab or a company

-   Efficient code that executes quickly...

-   A single environment/language for everything

<aside class="notes">
-   Rich collection of already existing **bricks**: we don't want to
    re-program the plotting of a curve, a Fourier transform or a fitting
    algorithm. Don't reinvent the wheel!

-   Easy to learn: computer science is neither our job nor our
    education. We want to be able to draw a curve, smooth a signal, do a
    Fourier transform in a few minutes.

-   Easy communication with collaborators, students, customers, to make
    the code live within a lab or a company: the code should be as
    readable as a book. Thus, the language should contain as few syntax
    symbols or unneeded routines as possible that would divert the
    reader from the mathematical or scientific understanding of the
    code.

-   Efficient code that executes quickly... but needless to say that a
    very fast code becomes useless if we spend too much time writing it.
    So, we need both a quick development time and a quick execution
    time.

-   A single environment/language for everything, if possible, to avoid
    learning a new software for each new problem.
</aside>



### Existing solutions

Which solutions do scientists use to work?

- Compiled languages: C, C++, Fortran
- Matlab
- Other scripting languages: Scilab, Octave, Igor, R, IDL, etc.



**Compiled languages: C, C++, Fortran, etc.**

-   Advantages:

    -   Very fast. Very optimized compilers. For heavy computations,
        it's difficult to outperform these languages.

    -   Some very optimized scientific libraries have been written for
        these languages. Example: BLAS (vector/matrix operations)

-   Drawbacks:

    -   Painful usage: no interactivity during development, mandatory
        compilation steps, verbose syntax (&, ::, }}, ; etc.), manual
        memory management (tricky in C). These are **difficult
        languages** for non computer scientists.



**Scripting languages: Matlab**

-   Advantages:

    -   Very rich collection of libraries with numerous algorithms, for
        many different domains. Fast execution because these libraries
        are often written in a compiled language.

    -   Pleasant development environment: comprehensive and well
        organized help, integrated editor, etc.

    -   Commercial support is available.

-   Drawbacks:

    -   Base language is quite poor and can become restrictive for
        advanced users.

    -   Not free.



**Other scripting languages: Scilab, Octave, Igor, R, IDL, etc.**

-   Advantages:

    -   Open-source, free, or at least cheaper than Matlab.

    -   Some features can be very advanced (statistics in R, figures in
        Igor, etc.)

-   Drawbacks:

    -   Fewer available algorithms than in Matlab, and the language is
        not more advanced.

    -   Some software are dedicated to one domain. Ex: Gnuplot or
        xmgrace to draw curves. These programs are very powerful, but
        they are restricted to a single type of usage, such as plotting.



**What about Python?**

-   Advantages:

    -   Very rich scientific computing libraries (a bit less than
        Matlab, though)

    -   Well thought out language, allowing to write very readable and
        well structured code: we "code what we think".

    -   Many libraries for other tasks than scientific computing (web
        server management, serial port access, etc.)

    -   Free and open-source software, widely spread, with a vibrant
        community.

-   Drawbacks:

    -   less pleasant development environment than, for example, Matlab.
        (More geek-oriented).

    -   Not all the algorithms that can be found in more specialized
        software or toolboxes.



### Tour of Scripts

Let's look at a few simple examples.



Hello Scientific World
```python
import math
r = math.pi / 2.0
s = math.sin(r)
print "Hello world, sin(%f)=%f" % (r,s)
```

Running in the shell:
```bash
$ python examples/intro/01_hello_world.py
Hello world, sin(1.570796)=1.000000
```



Input / Output
```python
import math
import os

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
infile = "numbers"
outfile = "f_numbers"

f = open(os.path.join(data_dir, infile), 'r')
g = open(os.path.join(data_dir, outfile), 'w')

def func(y):
    if y >= 0.0:
        return y**5.0*math.exp(-y)
    else:
        return 0.0
    
for line in f:
    line = line.split()
    x, y = float(line[0]), float(line[1])
    g.write("%g %12.5e\n" % (x,func(y)))
    
f.close(); g.close()
```



Input / Ouput Continued
```bash
$ cat examples/data/numbers 
1 2 
3 4 
5 6
7 8
9 10
$ python examples/intro/02_write_numbers.py
Read from examples/intro/../data/numbers
Wrote to examples/intro/../data/f_numbers
$ cat examples/data/f_numbers 
1  4.33073e+00
3  1.87552e+01
5  1.92748e+01
7  1.09924e+01
9  4.53999e+00
```



System commands

```python
 #!/usr/bin/env python
import sys,os
cmd = 'date'
output = os.popen(cmd)
lines = output.readlines()
fail = output.close()

if fail: print 'You do not have the date command'; sys.exit()

for line in lines:
    line = line.split()
    print "The current time is %s on %s %s, %s" %  (line[3],line[2],line[1],line[-1])   
```

```bash
$ ./examples/intro/03_call_sys_commands.py 
The current time is 11:50:25 on 24 Aug, 2013
```



Regular Expressions

```
@Book{Langtangen2011,
  author =    {Hans Petter Langtangen},
  title =     {A Primer on Scientific Programming with Python},
  publisher = {Springer},
  year =      {2011}
}
@Book{Langtangen2010,
  author =    {Hans Petter Langtangen},
  title =     {Python Scripting for Computational Science},
  publisher = {Springer},
  year =      {2010}
}
```



Regular Expressions Continued
```python
import os
import re

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
infile = os.path.join(data_dir, "python.bib")

pattern1 = "@Book{(.*),"
pattern2 = "\s+title\s+=\s+{(.*)},"

print "Reading from", infile
for line in file(infile):
    match = re.search(pattern1, line)
    if match: 
        print "Found a book with the tag '%s'" % match.group(1)

    match = re.search(pattern2, line)
    if match:
        print "The title is '%s'" % match.group(1)
```

```bash
$ python examples/intro/04_regular_expressions.py 
Reading from examples/intro/../data/python.bib
Found a book with the tag 'Langtangen2011'
The title is 'A Primer on Scientific Programming with Python'
Found a book with the tag 'Langtangen2010'
The title is 'Python Scripting for Computational Science'
```