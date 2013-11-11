#!/usr/bin/env python

import sys
import os

cmd = 'date'
output = os.popen(cmd)
lines = output.readlines()
fail = output.close()

if fail: print 'You do not have the date command'; sys.exit()

for line in lines:
    line = line.split()
    print "The current time is %s on %s %s, %s" %  (line[3],line[2],line[1],line[-1])   
