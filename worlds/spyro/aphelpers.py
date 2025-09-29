from enum import IntEnum
from collections.abc import Iterator

# type aliases
APLocationList = dict[str, int]
"""Archipelago requires locations be given in a specific format. This is that format.

This is a mapping from name to internal id.
"""

APLocationGroups = dict[str, set[str]]
"""Archipelago requires location groups be given in a specific format. This is that format.

This is a mapping from the name of the group to a set of the location names in that group.
"""

# constants
NO_ID_SET = -1
"""Arbitrary default value to signify no id was set"""

COUNTER_START_VALUE = 950
'''Location integer IDs must be well out of AP's reserve space.

AP reserves 0 downwards, but it never hurts to be extra sure.
'''

# Enums
class APDataType(IntEnum):
    UNKNOWN  = 0
    LOCATION = 1

# classes I consider to be used like structs
class APGroup():
    def __init__(self, name="INVALID GROUP"):
        self.name = name
        self.active = True

# classes I consider to be proper classes
class APData():
    def __init__(self):
        self.name:str = "THIS SHOULD BE AN INVALID LOCATION"
        self.type:APDataType = APDataType.UNKNOWN
        self.id:int = NO_ID_SET
        self.groups:list[APGroup] = []
        self.checked = False

    @property
    def active(self) -> bool:
        ret:bool = True
        
        for group in self.groups:
            if not group.active:
                ret = False
        
        return ret

    def _set_group_active_state(self, name:str, active:bool):
        for group in self.groups:
            if group.name == name:
                group.active = active
    
    def activate_group(self, name:str):
        self._set_group_active_state(name, True)
    
    def deactivate_group(self, name:str):
        self._set_group_active_state(name, False)
        
    def add_group(self, name:str):
        swp:APGroup = APGroup(name)
        
        missing:bool = True
        
        for group in self.groups:
            if group.name == name:
                missing = False
        
        if missing:
            self.groups.append(swp)

class APDataContainer():
    def __init__(self):
        self._contents:set[APData] = set()
        self._counter:int = COUNTER_START_VALUE
    
    def __contains__(self, key:int|str) -> bool:
        ret = False
        
        if isinstance(key, int):
            for item in self._contents:
                if item.id == key:
                    ret = True
        elif isinstance(key, str):
            for item in self._contents:
                if item.name == key:
                    ret = True
        else:
            raise TypeError("Key must be int or str!")

        return ret
    
    def __getitem__(self, key:int|str) -> APData:
        ret:APData = APData()
        found = False
        
        if isinstance(key, int):
            for item in self._contents:
                if item.id == key:
                    found = True
                    ret = item
        elif isinstance(key, str):
            for item in self._contents:
                if item.name == key:
                    found = True
                    ret = item
        else:
            raise TypeError("Key must be int or str!")
  
        if not found:
            raise KeyError("Not found!")
        
        return ret
    
    def __iter__(self) -> Iterator[APData]:
        return iter(self._contents)
    
    def add(self, val:APData) -> None:
        if val.name not in self:
            if val.id == NO_ID_SET:
                val.id = self._counter
            self._counter = self._counter + 1
            self._contents.add(val)
        
    def clear(self) -> None:
        self._contents.clear()
    
    def merge(self, other:"APDataContainer"):
        for data in other:
            self.add(data)
    
    def get_active(self) -> "APDataContainer":
        ret:APDataContainer = APDataContainer()
        
        for entry in self._contents:
            if entry.active:
                ret.add(entry)
        
        return ret
    
    def renumber(self) -> None:
        """Renumber entries, giving them each new ids.
        
        WARNING: If you do this without knowing what you're doing, you will
        break the DataPackage for the Archipelago session."""
        self._counter = COUNTER_START_VALUE
        
        for item in self:
            item.id = self._counter
            self._counter = self._counter + 1
       
    def to_ap_location_list(self) -> APLocationList:
        ret:APLocationList = {}
        
        for location in self:
            ret[location.name] = location.id
        
        return ret

    def to_ap_group_list(self) -> APLocationGroups:
        ret:APLocationGroups = {}
        
        for location in self:
            for group in location.groups:
                if group.name not in ret.keys():
                    ret[group.name] = set()
                ret[group.name].add(location.name)
        
        return ret
    
# define everything for lazy import
__all__ = [
    # type aliases
    "APLocationGroups",
    "APLocationList",
    
    # classes
    "APData",
    "APDataContainer",
    "APDataType",
    "APGroup",
]