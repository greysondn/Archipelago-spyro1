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

from appetite.validate.ap.guard import (
    Always,
    Never,
)

from appetite.validate.bh.datatype import (
    Int,
    String,
    Bytes,
)

Terminal = Union[
    Int,
    String,
    Bytes,
]

class And(BaseModel):
    type:Literal["and"]
    next:Sequence[Terminal]

class Or(BaseModel):
    type:Literal["or"]
    next:Sequence[Terminal]

Guard = Union[
    Always,
    Never,
    Terminal,
    And,
    Or,
]