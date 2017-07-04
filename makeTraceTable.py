#!/usr/bin/env python

import csv
import re
import sys

with open(sys.argv[1], "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    components = []
    for c in header:
        if "[" in c:
            component = c[0:c.index("[") - 1]
            if "&" in component:
                component = re.sub(r'\&', 'and', component)
            components.append(component)
    n = len(components)
    for row in reader:
        req = row[0]
        req = req[0:req.index("[") - 1]
        req = re.sub(r'\&', 'and', req)
        clist = []
        for i in range(1, n):
            if row[i]:
                clist.append(components[i])
        print("{} & {}".format(req, ", ".join(clist)))
