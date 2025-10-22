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

class Always(BaseModel):
    type:Literal["always"]

class Never(BaseModel):
    type:Literal["never"]

class Item(BaseModel):
    type:Literal["item"]
    name:str

Terminal = Union[
    Item,
]

class And(BaseModel):
    type:Literal["and"]
    next:Sequence[Terminal]

class Or(BaseModel):
    type:Literal["or"]
    next:Sequence[Terminal]

Guard = Union [
    Always,
    Never,
    And,
    Or,
]
