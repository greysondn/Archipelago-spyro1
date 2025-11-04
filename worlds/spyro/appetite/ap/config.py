"""
Module for things specific to configuration settings in ap's core
"""

from typing import (
    TypeVar,
)


ConfigType = TypeVar("ConfigType", bound="Config", default="Config", covariant=True)
"""TODO: Docs
"""

class Config():
    def __init__(self, name:str, value:object):
        self._name:str = name
        self._value:object = value