import sys

try:
    import pydantic
except ImportError:
    print("You must install pydantic to use this file!")
    print("maybe")
    print("pip install pydantic")
    print("or")
    print("pipenv install pydantic")
    print("?")
    # hard crash
    sys.exit(1)
    
from pydantic import (
    BaseModel,
    field_validator,
)

from typing import (
    List,
    Literal,
    Optional,
    Sequence,
    Union,
)

from appetite.validate.bh.datatype import DataType
from appetite.validate.bh.guard import Guard

IoType = Literal[
    "read",
    "write",
    "both",
    "none",
    None,
]

class Data(BaseModel):
    io:IoType
    data:DataType
    guards:Sequence[Guard]
