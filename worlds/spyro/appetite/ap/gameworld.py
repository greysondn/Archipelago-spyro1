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
    Generic,
)

class GameWorld(Generic[ContainerType, PlayerType]):
    def __init__(self, game:str):
        self._game = game
        self._roots:dict[str, ContainerType] = {}
        self._player:PlayerType | None = None