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

class Groups(BaseModel):
    entrances:Sequence[str]
    exits:Sequence[str]

class Mapping(BaseModel):
    entrance:str
    exits:Sequence[str]

class Preset:
    name:str
    mappings:Sequence[Mapping]

class Entrance(BaseModel):
    enabled:bool
    groups:Groups
    presets:list[Preset]