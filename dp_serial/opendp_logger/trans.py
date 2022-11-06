import opendp.transformations as trans 
from dp_serial.opendp_logger.mods import Transformation, wrapper

for f in dir(trans):
    if f[:5] == "make_":
        locals()[f] = wrapper(f, getattr(trans, f), 'trans')