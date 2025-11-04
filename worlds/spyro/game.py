# pure python version of Spyro stuff goes here
import appetite.ap as ap

from typing import (
    Any,
    Optional,
    cast,
    override,
)

class Config(ap.Config):
    pass

class Connection(
    ap.Connection[
        "Region"
    ]
):
    pass

class Hub(
    ap.Container[
        "Hub", # but not really
        "Level",
        "Region",
        "Item",
        "Location",
        Config
    ]
):
    def __init__(self):
        super().__init__("ERROR", "Spyro the Dragon")
        
        self._id:int = -1
    
    @override
    def set_from_data_yaml(self, data:dict[str, Any]) -> None:
        """Set data on this object from the expected strucutre in data.yaml

        Args:
            data: The parsed data.yaml structure
        """
        super().set_from_data_yaml(data)
        
        self.id = data["id"]
        # TODO: balloon addresses?
        # TODO: text offset?
        # TODO: total gems?
        # TODO: gem counter?
        # TODO: regions?
        # TODO: levels?
        # TODO: statue head checks?
    
    @classmethod
    def create_from_data_yaml(cls, data:dict[str, Any]) -> "Hub":
        """Create this from the expected data.yaml structure

        Args:
            data: The parsed data.yaml structure
        """
        ret:Hub = cls()
        ret.set_from_data_yaml(data)
        return ret
    
    @property
    def id(self) -> int:
        """Internal id value"""
        return self._id

    @id.setter
    def id(self, val:int) -> None:
        self._id = val
        
class Item(ap.Item):
    pass

class Level(
    ap.Container[
        "Hub",
        "Level", # but not really
        "Region",
        Item,
        "Location",
        Config
    ]
):
    pass

class Location(ap.Location):
    pass

class Player(
    ap.Player[
        Item
    ]
):
    pass

class Region(
    ap.Region[
        Connection
    ]
):
    pass

class World(
    ap.GameWorld[
        Hub,
        Player
    ]
):
    def __init__(self):
        super().__init__("Spyro the Dragon")
    
    @override
    def set_from_data_yaml(self, data:dict[str, Any]) -> None:
        """Set data on this object from the expected strucutre in data.yaml

        Args:
            data: The parsed data.yaml structure
        """
        # call super for base things
        super().set_from_data_yaml(data)
        
        # TODO: Vars?
        # TODO: Player?
        
        # Hubs?
        hubs = cast(list[dict[str, Any]], data["hubs"])
        for hub in hubs:
            swp:Hub = Hub.create_from_data_yaml(data)
            swp.set_from_data_yaml(data)
            self.roots.append(swp)
    
    @classmethod
    def create_from_data_yaml(cls, data:dict[str, Any]) -> "World":
        """Create this from the expected data.yaml structure

        Args:
            data: The parsed data.yaml structure
        """
        ret:World = cls()
        ret.set_from_data_yaml(data)
        return ret