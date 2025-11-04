"""
Module for things specific to AP Locations.
"""

from appetite.ap.core import (
    CollectionState,
)

from appetite.ap.manager import (
    IndexManager,
)

from typing import (
    Any,
    Callable,
    TypeVar,
)

LocationType = TypeVar("LocationType", bound="Location", default="Location", covariant=True)
"""TODO: Docs
"""


class Location():
    """TODO: Docs
    """
    def __init__(self, game:str):
        """TODO: Docs
        """
        self._active:bool = True
        self._name:str = ""
        self._virtual:bool = True
        self._id:int = IndexManager().get_next(game)
        self._groups:set[str] = set()
        self._checked:bool = False
        self._guard:Callable[[CollectionState], bool] = lambda state: True
    
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