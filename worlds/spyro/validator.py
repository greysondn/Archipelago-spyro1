# So, this validator requires pydantic.
# pip install pydantic
# or, if you're a good [girl/boy/etc] what never did wrong
# pipenv install pydantic
#
# We observed there was no need to make pydantic a hard requirement in the
# archipelago distribution, because it's only used as a development library.
#

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
    Union
)

# -----------------------------------
# AP GUARDS
# -----------------------------------
class Ap_guard_always(BaseModel):
    type:Literal["always"]

class Ap_guard_never(BaseModel):
    type:Literal["never"]

class Ap_guard_item(BaseModel):
    type:Literal["item"]
    name:str

Ap_guard_terminal = Union[
    Ap_guard_item,
]

class Ap_guard_and(BaseModel):
    type:Literal["and"]
    next:Sequence[Ap_guard_terminal]

class Ap_guard_or(BaseModel):
    type:Literal["or"]
    next:Sequence[Ap_guard_terminal]

Ap_guard = Union[
    Ap_guard_always,
    Ap_guard_never,
    Ap_guard_and,
    Ap_guard_or,
]

# ------------------------------------
# AP ITEMS
# ------------------------------------

Ap_item_category = Literal[
    "progression",
    "trap",
    "filler",
    "useful",
    "skip_balancing",
    # if you can't figure out "progression_skip_balancing",
    # it's not me, it's you.
]

class Ap_item_count_abs(BaseModel):
    abs:int
    min:Optional[int]
    max:Optional[int]
    weight:Optional[Literal[0]]
    
    @field_validator("abs", mode="after")
    def validate_abs(cls, value:int) -> int:
        if value < 0:
            raise ValueError("abs must be greater than or equal to zero")
        return value
    
    @field_validator("weight", mode="after")
    def validate_weight(cls, value:Literal[0]) -> Literal[0]:
        if value != 0:
            raise ValueError("weight must be 1 or omitted")
        return value
    
    @field_validator("min", "max", mode="after")
    def validate_your_fat_momma(cls, value:int, values) -> int:
        if value != values["abs"]:
            raise ValueError("min and max must be omitted or equal to abs!")
        return value

# TODO: Define next
Ap_item_count_weighted

class Ap_item(BaseModel):
    name:str
    count:COMPLEX # todo
    categories:Sequence[Ap_item_category]
    aliases:Sequence[str]
    groups:Sequence[str]



# I don't know all the domains for every system
# so this is a "grow as you go" kind of thing
bh_memory_domain = Literal[
    "MainRAM",
]

bhdata_type_io = Literal["read", "write", "both", "none", None]

class Bh_data_type_data_type_flag(BaseModel):
    address:int
    length:Optional[Literal[1]]
    type:Literal["flag"]
    domain:bh_memory_domain
    value:Literal[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
    
    @field_validator("length", mode="after")
    def validate_length(cls, value:Literal[1]) -> Literal[1]:
        if value != 1:
            raise ValueError("length must be 1 or omitted")
        return value

class Bh_data_type_data_type_int(BaseModel):
    address:int
    length:int
    type:Literal["int"]
    domain:bh_memory_domain
    value:int

class Bh_data_type_data_type_string(BaseModel):
    address:int
    length:int
    type:Literal["string"]
    domain:bh_memory_domain
    value:str

class Bh_data_type_data_type_bytes(BaseModel):
    address:int
    length:int
    type:Literal["bytes"]
    domain:bh_memory_domain
    value:Sequence[int]

Bh_data_type_data_type = Union[
    Bh_data_type_data_type_flag,
    Bh_data_type_data_type_int,
    Bh_data_type_data_type_string,
    Bh_data_type_data_type_bytes,
]

Bh_guard_terminal = Union[
    Bh_data_type_data_type_int,
    Bh_data_type_data_type_string,
    Bh_data_type_data_type_bytes,
]

class Bh_guard_and(BaseModel):
    type:Literal["and"]
    next:Sequence[Bh_guard_terminal]

class Bh_guard_or(BaseModel):
    type:Literal["or"]
    next:Sequence[Bh_guard_terminal]

Bh_guard = Union[
    Ap_guard_always,
    Ap_guard_never,
    Bh_guard_terminal,
    Bh_guard_and,
    Bh_guard_or,
]

class Bh_data(BaseModel):
    io:bhdata_type_io
    data:Bh_data_type_data_type
    guard:Bh_guard

class Bh_item(Ap_item):
    bizhawk:Bh_data









class Spyro_world(BaseModel):
    items:Sequence[Bh_item]



class Spyro_root(BaseModel):
    game:Literal["Spyro the Dragon"]
    
    world:Spyro_world