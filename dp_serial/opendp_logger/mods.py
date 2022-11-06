from typing import get_type_hints, Union
from opendp import Transformation, Measurement
import opendp as opendp
import json

import pkg_resources

# OPENDP version
OPENDP_VERSION = pkg_resources.get_distribution("opendp").version

# allow dumps to serialize object types
class DPL_Encoder(json.JSONEncoder):
  def default(self, obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, type):
        serial = "py_type:"+obj.__name__
        return serial
    return obj.__dict__

  def encode(self, obj) -> str:
    def hint_tuples(item):
        if isinstance(item, tuple):
            return {'_tuple': True, '_items': [hint_tuples(e) for e in item]}
        if isinstance(item, list):
            return [hint_tuples(e) for e in item]
        if isinstance(item, dict):
            return {key: hint_tuples(value) for key, value in item.items()}
        else:
            return item

    return super().encode(hint_tuples(obj))

# export to json
def to_json(self):
    return json.dumps(
        {
            "version": OPENDP_VERSION,
            "ast": self.ast
        },
        cls=DPL_Encoder
    )

def wrapper(f_str, f, module_name):
    def wrapped(*args, **kwargs):
        ret_trans = f(*args, **kwargs)

        args = list(args)
        for i in range(len(args)):
            if type(args[i]) == Transformation or type(args[i]) == Measurement:
                args[i] = args[i].ast
        args = tuple(args)

        for k, v in kwargs.items():
            if type(v) == Transformation or type(v) == Measurement:
                kwargs[k] = v.ast

        ret_trans.ast = {
            "func": f_str,
            "module": module_name,
            "type": get_type_hints(f)['return'].__name__,
            "args": args,
            "kwargs": kwargs
        }

        return ret_trans

    wrapped.__annotations__ = f.__annotations__

    return wrapped

def Measurement__rshift__(self, other: "Transformation"):
    if isinstance(other, Transformation):
        from .comb import make_chain_tm
        return make_chain_tm(other, self)

    raise ValueError(f"rshift expected a transformation, got {other}")

def Transformation__rshift__(self, other: Union["Measurement", "Transformation"]):
    if isinstance(other, Measurement):
        from .comb import make_chain_mt
        return make_chain_mt(other, self)

    if isinstance(other, Transformation):
        from .comb import make_chain_tt
        return make_chain_tt(other, self)

    raise ValueError(f"rshift expected a measurement or transformation, got {other}")

Transformation = opendp.Transformation
Measurement = opendp.Measurement

Transformation.ast = None
#copy_rshift = Transformation.__rshift__
Transformation.__rshift__ = Transformation__rshift__
Measurement.__rshift__ = Measurement__rshift__

Transformation.to_json = to_json
Measurement.to_json = to_json
