from math import *
from random import *
from console import Console
c = Console()

import datetime

try:
    import flatlatex
    latex = flatlatex.converter()
    print(latex.convert(r'\forall \eta>0, \exists n\in\mathbb {N}, \forall i>n, |u_i-\mathcal {l}|<\eta'))
except:
    c.out("warning", "flatlatex is missing", "Missing modules")