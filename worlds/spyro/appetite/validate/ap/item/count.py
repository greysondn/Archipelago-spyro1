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

class Abs(BaseModel):
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
    def validate_min_and_max(cls, value:int, values) -> int:
        if value != values["abs"]:
            raise ValueError("min and max must be omitted or equal to abs!")
        return value
    
class Weighted(BaseModel):
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