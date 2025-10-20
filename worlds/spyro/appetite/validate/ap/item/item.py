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

Category = Literal[
    "progression",
    "trap",
    "filler",
    "useful",
    "skip_balancing",
    # if you can't figure out "progression_skip_balancing",
    # it's not me, it's you.
]

class Item(BaseModel):
    name:str
    # count:COMPLEX # TODO
    categories:Sequence[Category]
    aliases:Sequence[str]
    groups:Sequence[str]