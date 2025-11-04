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

class GameWorld[ContainerType, PlayerType]:
    def __int__(self, game:str):
        self._game = game
        self._roots:dict[str, ContainerType] = {}
        self._player:PlayerType | None = None