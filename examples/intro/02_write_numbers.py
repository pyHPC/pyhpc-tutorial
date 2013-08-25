#!/usr/bin/env python

import math
import os

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
infile = os.path.join(data_dir, "numbers")
outfile = os.path.join(data_dir, "f_numbers")

f = open(infile, 'r')
g = open(outfile, 'w')

def func(y):
    if y >= 0.0:
        return y**5.0*math.exp(-y)
    else:
        return 0.0


print "Read from", infile
    
for line in f:
    line = line.split()
    x, y = float(line[0]), float(line[1])
    g.write("%g %12.5e\n" % (x,func(y)))

print "Wrote to", outfile
f.close(); g.close()
