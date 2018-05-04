#!/usr/bin/env python

import csv
import re
import sys

with open(sys.argv[1], "r") as f:
    reader = csv.reader(f)

    # Extract component list from first (header) line
    header = next(reader)
    components = []
    for c in header:
        # Separate component from package
        component = c.split(" [")[0]
        # Protect ampersand from LaTeX and make readable
        component = re.sub(r'\&', 'and', component)
        # Remove leading digits used for sort ordering
        component = re.sub(r'^\d+\s+', '', component)
        components.append(component)
    n = len(components)

    # Each succeeding line corresponds to a requirement
    for row in reader:
        req = row[0]
        # Separate requirement from package
        req = req.split(" [")[0]
        # Protect ampersand from LaTeX and make readable
        req = re.sub(r'\&', 'and', req)
        # Remove digits after req id used for sort ordering
        req = re.sub(r'\s+\d+', '', req)
        clist = []
        for i in range(1, n):
            if row[i]:
                clist.append(components[i])
        print("{} & {}".format(req, ", ".join(clist)))
