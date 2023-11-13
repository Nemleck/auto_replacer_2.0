from math import *
from random import *

import datetime

def get_time():
    now = datetime.datetime.utcnow()
    return now.hour, now.minute, now.second

try:
    import flatlatex
    latex = flatlatex.converter()
    print(latex.convert(r'\forall \eta>0, \exists n\in\mathbb {N}, \forall i>n, |u_i-\mathcal {l}|<\eta'))
except:
    time = get_time()
    print(f"[{time[0]}:{time[1]}:{time[2]}] [Missing modules] flatlatex is missing")