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
    Discriminator,
    Tag,
    ValidationError,
    field_validator,
)

from pydantic_core import (
    core_schema,
)

from typing import (
    Annotated,
    Any,
    cast,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
)

# I don't know all the domains for every system
# so this is a "grow as you go" kind of thing
MemoryDomain = Literal[
        "MainRAM",
]

class Flag(BaseModel):
    address:int
    length:Optional[Literal[1]] = None
    type:Literal["flag"]
    domain:MemoryDomain
    value:Literal[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
    
    @field_validator("length", mode="after")
    def validate_length(cls, value:Literal[1]) -> Literal[1]:
        if value != 1:
            raise ValueError("length must be 1 or omitted")
        return value

class Int(BaseModel):
    address:int
    length:int
    type:Literal["int"]
    domain:MemoryDomain
    value:int

class String(BaseModel):
    address:int
    length:int
    type:Literal["string"]
    domain:MemoryDomain
    value:str
    
class Bytes(BaseModel):
    address:int
    length:int
    type:Literal["bytes"]
    domain:MemoryDomain
    value:Sequence[int]

def discriminate_datatype(value:Any) -> Optional[str]:
    ret:Optional[str] = None
    
    if isinstance(value, dict):
        match value["type"]:
            case "flag":
                ret = "flag"
            case "int":
                ret = "int"
            case "string":
                ret = "string"
            case "bytes":
                ret = "bytes"
            case _:
                ret = None
    
    return ret

DataType = Annotated[
    Union[
        Annotated[Flag, Tag("flag")],
        Annotated[Int, Tag("int")],
        Annotated[String, Tag("string")],
        Annotated[Bytes, Tag("bytes")]
    ],
    Discriminator(
        discriminate_datatype,
        custom_error_type = "invalid_bh_datatype",
        custom_error_message = "Invalid Bizhawk DataType",
        custom_error_context = {"discriminator":"type"}
    )
]