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
    ItemClassification as APItemClassification,
)

# type vars
APContainerType = TypeVar("APContainerType", bound="APContainer", default="APContainer", covariant=True)
APParentContainerType = TypeVar("APParentContainerType", bound="APContainer", default="APContainer", covariant=True)
APRegionType = TypeVar("APRegionType", bound="APRegion", default="APRegion", covariant=True)
APRegionTypeLeft = TypeVar("APRegionTypeLeft", bound="APRegion", default="APRegion", covariant=True)
APRegionTypeRight = TypeVar("APRegionTypeRight", bound="APRegion", default="APRegion", covariant=True)
APDoorType = TypeVar("APDoorType", bound="APDoor", default="APDoor", covariant=True)
APLocationType = TypeVar("APLocationType", bound="APLocation", default="APLocation", covariant=True)
APItemType = TypeVar("APItemType", bound="APItem", default="APItem", covariant=True)
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

class APContainer(Generic[APParentContainerType, APContainerType, APRegionType, APDoorType, APItemType, APLocationType, APConfigType]):
    def __init__(self, name:str, game:str):
        self._game:str = game
        self._parent:APParentContainerType | None = None
        self._children:list[APContainerType] = []
        self._regions:list[APRegionType] = []
        self._doors:list[APDoorType] = []
        self._items:list[APItemType] = []
        self._locations:list[APLocationType] = []
        self._configs:list[APConfigType] = []  
        self._name:str = name
        self._id:int = APIndexManager().get_next(game)
        
    @property
    def items(self) -> list[APItemType]:
        return self._items
        
    @property
    def locations(self) -> list[APLocationType]:
        return self._locations
    
    def _traverse(
        self,
        algorithm:"APTraversalAlgorithm[R]",
        seq:str,
        recurse:bool = False,
        include_virtual:bool = False,
    ) -> list[R]:
        ret:list[R] = []
        
        ret = algorithm(self, seq, ret, include_virtual)
        
        if recurse:
            for child in self._children:
                ret = algorithm(child, seq, ret, include_virtual)
        
        return ret

    def find_item_by_name(self, name:str, recurse:bool, include_virtual:bool) -> APItemType:
        algorithm:SearchPropertyAlgorithm[APItemType] = SearchPropertyAlgorithm("name", name)
        return self._traverse(algorithm, "items", recurse, include_virtual)[0]
    
    def find_item_by_id(self, id:int, recurse:bool, include_virtual:bool) -> APItemType:
        algorithm:SearchPropertyAlgorithm[APItemType] = SearchPropertyAlgorithm("id", id)
        return self._traverse(algorithm, "items", recurse, include_virtual)[0]
    
    def find_location_by_name(self, name:str, recurse:bool, include_virtual:bool) -> APLocationType:
        algorithm:SearchPropertyAlgorithm[APLocationType] = SearchPropertyAlgorithm("name", name)
        return self._traverse(algorithm, "locations", recurse, include_virtual)[0]
    
    def find_location_by_id(self, id:int, recurse:bool, include_virtual:bool) -> APLocationType:
        algorithm:SearchPropertyAlgorithm[APLocationType] = SearchPropertyAlgorithm("id", id)
        return self._traverse(algorithm, "locations", recurse, include_virtual)[0]

    def build_ap_location_list(self):
        algorithm:APBuildNameToIdListAlgorithm = APBuildNameToIdListAlgorithm()
        return self._traverse(algorithm, "locations", True, False)[0]

    def build_ap_item_list(self):
        algorithm:APBuildNameToIdListAlgorithm = APBuildNameToIdListAlgorithm()
        return self._traverse(algorithm, "items", True, False)[0]
    
    def build_ap_location_group_list(self):
        algorithm:APBuildGroupAlgorithm = APBuildGroupAlgorithm()
        return self._traverse(algorithm, "locations", True, False)[0]
    
    def build_ap_item_group_list(self):
        algorithm:APBuildGroupAlgorithm = APBuildGroupAlgorithm()
        return self._traverse(algorithm, "items", True, False)[0]

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
        
class APIndexManager(object):
    _instance:"APIndexManager | None" = None
    """The only instance of this class"""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIndexManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # We would like to present to you some forbidden, black magic that will
        # make you scream "NO! THAT NOT ONLY DOESN'T GO THERE, BUT IT SHOULDN'T
        # EVER WORK! NO! NO! NO! NO!"
        if not hasattr(self, "_initialized"):
            # do init
            self._initialized:bool = True
            """Whether or not this has been initialized."""
            
            self._current:dict[str,int] = {}
    
    def get_next(self, game:str) -> int:
        """Get the next valid int out of this manager.
        
        The manager maintains per-game indexes based on their names. Two games
        will have two different indexes.
        
        Args:
            game: Which game this is for. 
        """
        ret:int = self._current.get(game, 1)
        
        self._current[game] = ret + 1
        
        return ret

class APItem():
    def __init__(self, game:str):
        self._active:bool = True
        self._classification:APItemClassification = APItemClassification(0)
        self._name:str = ""
        self._id:int = APIndexManager().get_next(game)
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

# Traversal algorithm classes

class APTraversalAlgorithm(Protocol[R]):
    def __call__(self, node:APContainer, seq:str, results_so_far:list[R], include_virtual:bool) -> list[R]:
        ...

class SearchAlgorithm(Generic[R]):
    def __init__(self, value:object):
        """Init.
        
        Args:
            value: VAlue we're searching for in sequences
        """
        
        self.value:object = value
        """Value we're searching for in sequences"""

    def __call__(self, node:APContainer, seq:str, results_so_far:list[R], include_virtual:bool) -> list[R]:
        ret:list[R] = results_so_far
        container:list[R] = getattr(node, seq)
        
        for item in container:
            is_virtual:bool = getattr(item, "virtual")
            
            if item == self.value:
                if not is_virtual:
                    ret.append(item)
                if is_virtual and include_virtual:
                    ret.append(item)
        
        return ret

class SearchPropertyAlgorithm(Generic[R]):
    def __init__(self, prop:str, value:object):
        """Init.
        
        Args:
            prop: Name of the property that we're searching
            value: The value we want that property to have
        """
        
        self.prop:str = prop
        """Name of the property that we're searching"""
        
        self.value:object = value
        """The value we want that property to have"""
        
    def __call__(self, node:APContainer, seq:str, results_so_far:list[R], include_virtual:bool) -> list[R]:
        ret:list[R] = results_so_far
        container:list[R] = getattr(node, seq)
        
        for item in container:
            if getattr(item, self.prop) == self.value:
                is_virtual:bool = getattr(item, "virtual")
            
                if item == self.value:
                    if not is_virtual:
                        ret.append(item)
                    if is_virtual and include_virtual:
                        ret.append(item)
        
        return ret
    
class APBuildNameToIdListAlgorithm():
    def __call__(self, node:APContainer, seq:str, results_so_far:list[dict[int, str]], include_virtual:bool) -> list[dict[int, str]]:
        ret:list[dict[int, str]] = results_so_far
        
        if len(ret) < 1:
            ret.append({})
        
        listing:dict[int, str] = {}
        
        for item in getattr(node, seq):
            is_virtual:bool = getattr(item, "virtual")
            
            if not is_virtual:
                listing[item.id] = item.name
        
        ret[0].update(listing)
        
        return ret

class APBuildGroupAlgorithm():
    def __call__(self, node:APContainer, seq:str, results_so_far:list[dict[str, set[str]]], include_virtual:bool) -> list[dict[str, set[str]]]:
        ret:list[dict[str, set[str]]] = results_so_far
        
        if len(ret) < 1:
            ret.append({})
        
        group_dict:dict[str, set[str]] = ret[0]
        
        for item in getattr(node, seq):
            for group in item.groups:
                if group not in group_dict:
                    group_dict[group] = set()
                group_dict[group].add(item.name)
        
        ret[0] = group_dict
        
        return ret
