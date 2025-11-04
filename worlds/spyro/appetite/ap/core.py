"""
This module covers things that are in Archipelago itself. That is to say, things
that are part of the core Archipelago code.

Most of it should be type aliases and protocols.
"""

from enum import (
    auto,
    IntFlag,
)

from typing import (
    Counter,
    Dict,
    Optional,
    Protocol,
    Set,
)

# ---------
# protocols
# ---------
class Location(Protocol):
    """TODO: Document
    """
    game: str
    address: Optional[int]

class CollectionState(Protocol):
    """TODO: Document
    """
    prog_items: Dict[int, Counter[str]]
    locations_checked: Set[Location]

# ------------
# type aliases
# ------------
LocationList = Dict[str, int]
"""Dict[name:str, id:int]

Archipelago requires locations be given in a specific format. This is that format.

This is a mapping from name to internal id.
"""

LocationGroups = Dict[str, Set[str]]
"""dict[name:str, locations:set[str]]

Archipelago requires location groups be given in a specific format. This is that format.

This is a mapping from the name of the group to a set of the location names in that group.
"""

