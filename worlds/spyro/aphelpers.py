from typing import TypeVar

from appetite.ap.manager import (
    IndexManager as APIndexManager,
)

# type vars

APConfigType = TypeVar("APConfigType", bound="APConfig", default="APConfig", covariant=True)
APPlayerType = TypeVar("APPlayerType", bound="APPlayer", default="APPlayer", covariant=True)

# actual classes (except traversal algorithms)

class APConfig(): # probably a template of some type
    def __init__(self, game:str):
        self._id:int = APIndexManager().get_next(game)
        self._name:str = ""
        self._value:object = object()




class APGameWorld[APContainerType, APPlayerType]:
    def __int__(self, game:str):
        self._game = game
        self._roots:dict[str, APContainerType] = {}
        self._player:APPlayerType | None = None





class APPlayer[APItemType]():
    def __init__(self, game:str):
        self._id:int = APIndexManager().get_next(game)
        self._name:str = ""
        self._inventory:list[APItemType] = []

