import opendp.measurements as meas 
from dp_serial.opendp_logger.mods import Measurement, wrapper

for f in dir(meas):
    if f[:5] == "make_":
        locals()[f] = wrapper(f, getattr(meas, f), 'meas')