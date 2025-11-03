from appetite.ap.manager import IndexManager

from enum import (
    IntFlag,
    auto,
)

from typing import (
    TypeVar,
)

ItemType = TypeVar("ItemType", bound="Item", default="Item", covariant=True)
"""TypeVar for AP Item types.

It's anticipated that maybe we'd need to retrieve the underlying type of an
inherited item in our object structure, so a typevar became necessary to specify
the constraints.
"""


class ItemClassification(IntFlag):
    """
    Archipelago uses bitwised Item classifications, so this is a way to
    represent that structure.
    """
    filler         = auto()
    progression    = auto()
    useful         = auto()
    trap           = auto()
    skip_balancing = auto()
    deprioritized  = auto()

class Item():
    """An item, compatible with Archipelago.
    """
    def __init__(self, game:str):
        self._active:bool = True
        self._classification:ItemClassification = ItemClassification(0)
        self._name:str = ""
        self._id:int = IndexManager().get_next(game)
        self._groups:set[str] = set()
        self._number_obtained:int = 0
        self._virtual:bool = False
    
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