"""
Module for things directly affecting containers for AP.

You can think of these as the overarching structural pieces - worlds, games, and
levels.
"""

class APContainer(Generic[APParentContainerType | None, APContainerType, APRegionType, APDoorType, APItemType, APLocationType, APConfigType]):
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
