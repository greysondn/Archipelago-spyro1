"""
Module to hold the core gameworld representation.

Not much to it, is there?
"""

from appetite.ap.container import (
    ContainerType,
)

from appetite.ap.player import (
    PlayerType,
)

from typing import (
    Any,
    Generic,
)

class GameWorld(Generic[ContainerType, PlayerType]):
    def __init__(self, game:str):
        self.game = game
        self._roots:list[ContainerType] = []
        self._player:PlayerType | None = None
        
    def set_from_data_yaml(self, data:Any) -> None:
        """Set data on this object from the expected strucutre in data.yaml

        Args:
            data: The parsed data.yaml structure
        """
        self.game = data["game"]
        
    @property
    def game(self) -> str:
        return self.game
    
    @game.setter
    def game(self, val:str) -> None:
        self.game = val
    
    @property
    def roots(self) -> list[ContainerType]:
        return self._roots
    
    @property
    def player(self) -> PlayerType | None:
        return self.player