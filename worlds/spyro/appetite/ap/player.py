"""
Module for things specific to player's data in AP

"""

from appetite.ap.item import (
    ItemType,
)

from typing import (
    Generic,
    TypeVar,
)

PlayerType = TypeVar("PlayerType", bound="Player", default="Player", covariant=True)
"""TODO: Docs
"""


class Player(Generic[ItemType]):
    """TODO: Docs
    """
    def __init__(self, id:int = -1, name:str = "ERROR"):
        """TODO: Docs
        """
        self._id:int = id
        self._name:str = name
        self._inventory:list[ItemType] = []