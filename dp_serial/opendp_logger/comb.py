import opendp.combinators as comb 
from .mods import wrapper

for f in dir(comb):
    if f[:5] == "make_":
        locals()[f] = wrapper(f, getattr(comb, f), 'comb')