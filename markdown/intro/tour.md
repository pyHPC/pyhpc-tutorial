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
