"""
Module for things specifically affecting AP regions.
"""

from appetite.ap.core import (
    CollectionState,
)

from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
)

RegionType = TypeVar("RegionType", bound="Region", default="Region", covariant=True)
ConnectionType = TypeVar("ConnectionType", bound="Connection", default="Connection", covariant=True)

class HalfConnection[RegionType]:
    """TODO: Docs
    """
    def __init__(self, name:str, region:RegionType, group:str):
        """TODO: Docs
        """
        self._name:str = name
        self._region:RegionType = region
        self._group:str = group
        self._guard:Callable[[CollectionState], bool] = lambda state: True

class Connection[RegionType]():
    """TODO: Docs
    """
    def __init__(self, name:str, shuffle:bool, src_region:RegionType, src_group:str, dst_region:RegionType, dst_group:str, src_name:Optional[str] = None, dst_name:Optional[str] = None):
        """TODO: Docs
        """
        self._name:str = name
        self._shuffle:bool = shuffle
        
        _src_name:str|None = src_name 
        if _src_name is None:
            _src_name = self.name + " src"
        
        _dst_name:str|None = dst_name
        if _dst_name is None:
            _dst_name = self.name + " dst"
        
        self._src:HalfConnection = HalfConnection[RegionType](_src_name, src_region, src_group)
        self._dst:HalfConnection = HalfConnection[RegionType](_dst_name, dst_region, dst_group)
    
    @property
    def name(self) -> str:
        return self._name
    
class Region[ConnectionType]():
    def __init__(self, name:str):
        self._name:str = name
        self._entrances:list[ConnectionType] = []
        self._exits:list[ConnectionType] = []
        self._guard:Callable[[CollectionState], bool] = lambda state: True

    def set_from_data_yaml(self, data:dict[str, Any]) -> None:
        """Set data on this object from the expected strucutre in data.yaml

        Args:
            data: The parsed data.yaml structure
        """
        self.name = data["name"]
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, val:str):
        self._name = val