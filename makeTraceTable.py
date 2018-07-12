#!/usr/bin/env python

import csv
import re
import sys

with open(sys.argv[1], "r") as f:
    reader = csv.reader(f)

    # Extract component list from first (header) line
    header = next(reader)
    components = []
    component_reqs = dict()
    for c in header:
        # Separate component from package
        component = c.split(" [")[0]
        # Protect ampersand and underscore from LaTeX and make readable
        component = re.sub(r'\&', 'and', component)
        component = re.sub(r'_', '\\_', component)
        # Remove leading digits used for sort ordering
        component = re.sub(r'^\d+\s+', '', component)
        components.append(component)
        component_reqs[component] = []
    n = len(components)


    print(r"""
\newpage
\section{Appendix: Traceability}\label{appendix-traceability}

\subsection{Requirement to Component
Traceability}\label{requirement-to-component-traceability}

\footnotesize
\begin{longtable}{p{0.4\textwidth}p{0.55\textwidth}}
\hline
\multicolumn{1}{c}{\textbf{Requirement}} &
\multicolumn{1}{c}{\textbf{Components}} \\ \hline
\endhead
""")

    # Each succeeding line corresponds to a requirement
    for row in reader:
        req = row[0]
        # Separate requirement from package
        req = req.split(" [")[0]
        # Protect ampersand from LaTeX and make readable
        req = re.sub(r'\&', 'and', req)
        # Remove digits after req id used for sort ordering
        req = re.sub(r'([A-Z]-\d+)\s+\d+', r'\1', req)
        clist = []
        for i in range(1, n):
            if row[i]:
                clist.append(components[i])
                component_reqs[components[i]].append(req)
        print("{} & {} \\\\ \\hline".format(req, ", ".join(clist)))


print(r"""
\end{longtable}
\normalsize

\subsection{Component to Requirement
Traceability}\label{component-to-requirement-traceability}

Note that only ``leaf'' components are traced to requirements.

\setitemize{noitemsep,topsep=0pt,parsep=0pt,partopsep=0pt}
\footnotesize
""")

for component in components:
    if len(component_reqs[component]) == 0:
        continue
    print(component + r" \begin{itemize}" + \
            "\n\\item " + \
            "\n\\item ".join(component_reqs[component]) + \
            "\n" + r"\end{itemize}")
