from collections import Counter
from collections.abc import Sequence
from enum import auto
from enum import IntFlag
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Literal
from typing import Optional
from typing import Protocol
from typing import Set
from typing import Type
from typing import TypeVar

from appetite.ap.core import (
    CollectionState as APCoreCollectionState,
)

from appetite.ap.manager import (
    IndexManager as APIndexManager,
)

# type varsAPRegionType = TypeVar("APRegionType", bound="APRegion", default="APRegion", covariant=True)
APRegionTypeLeft = TypeVar("APRegionTypeLeft", bound="APRegion", default="APRegion", covariant=True)
APRegionTypeRight = TypeVar("APRegionTypeRight", bound="APRegion", default="APRegion", covariant=True)
APDoorType = TypeVar("APDoorType", bound="APDoor", default="APDoor", covariant=True)
APLocationType = TypeVar("APLocationType", bound="APLocation", default="APLocation", covariant=True)
APConfigType = TypeVar("APConfigType", bound="APConfig", default="APConfig", covariant=True)
APPlayerType = TypeVar("APPlayerType", bound="APPlayer", default="APPlayer", covariant=True)

T = TypeVar("T", covariant=True)
"""Fundamental type stored in a sequence"""

S = TypeVar("S", covariant=True)
"""type of a sequence"""

R = TypeVar("R")
"""Return type of a method"""

# actual classes (except traversal algorithms)

class APConfig(): # probably a template of some type
    def __init__(self, game:str):
        self._id:int = APIndexManager().get_next(game)
        self._name:str = ""
        self._value:object = object()



class APDoor[APRegionTypeLeft, APRegionTypeRight]():
    def __init__(self, left:APRegionTypeLeft, right:APRegionTypeRight, game:str):
        self._name:str = ""
        self._index:int = APIndexManager().get_next(game)
        self._left:APRegionTypeLeft = left
        self._right:APRegionTypeRight = right
        self._guard_forwards:Callable[[APCoreCollectionState], bool] = lambda state: True
        self._guard_backwards:Callable[[APCoreCollectionState], bool] = lambda state: True
    
class APGameWorld[APContainerType, APPlayerType]:
    def __int__(self, game:str):
        self._game = game
        self._roots:dict[str, APContainerType] = {}
        self._player:APPlayerType | None = None



class APLocation():
    def __init__(self, game:str):
        self._active:bool = True
        self._name:str = ""
        self._virtual:bool = True
        self._id:int = APIndexManager().get_next(game)
        self._groups:set[str] = set()
        self._checked:bool = False
        self._guard:Callable[[APCoreCollectionState], bool] = lambda state: True
    
    @property
    def virtual(self) -> bool:
        return self._virtual
    
    @virtual.setter
    def virtual(self, val:bool):
        self._virtual = val
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, val:str):
        self._name = val
        
    @property
    def groups(self) -> set[str]:
        return self._groups

class APPlayer[APItemType]():
    def __init__(self, game:str):
        self._id:int = APIndexManager().get_next(game)
        self._name:str = ""
        self._inventory:list[APItemType] = []

class APRegion[APDoorType]():
    def __init__(self, game:str):
        self._name:str = ""
        self._index:int = APIndexManager().get_next(game)
        self._entrances:list[APDoorType] = []
        self._exits:list[APDoorType] = []
        guard:Callable[[APCoreCollectionState], bool] = lambda state: True