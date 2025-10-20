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

from appetite.validate.bh.item import Item

class Spyro_world(BaseModel):
    items:Sequence[Item]

class Spyro_root(BaseModel):
    game:Literal["Spyro the Dragon"]
    
    world:Spyro_world