#!/usr/bin/env python

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
