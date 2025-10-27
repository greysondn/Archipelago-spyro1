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

from appetite.validate.ap.guard import Guard

class ConnectionGroups(BaseModel):
    src:str
    dst:str

class ConnectionGuards(BaseModel):
    src:Guard
    dst:Guard

class Connection(BaseModel):
    # source is always "this"
    dst:str
    shuffle:bool
    guard:ConnectionGuards
    group:ConnectionGroups
    
class Location(BaseModel):
    name:str
    groups:Sequence[str]
    guard:Guard

class Region(BaseModel):
    name:str
    locations:Sequence[Location]
    guard:Guard
    connections:Sequence[Connection]