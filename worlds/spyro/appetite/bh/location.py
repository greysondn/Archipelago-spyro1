"""
module for bizhawk location stuff as it relates to AP.
"""

from appetite.ap.location import (
    Location as APLocation,
)

from appetite.bh.core import (
    EndianType,
)

from appetite.bh.memory import (
    MemoryEntry,
)

class Location(APLocation):
    """An APLocation, with extras for Bizhawk implementations"""
    def __init__(self, game:str, address:int, length:int, region:str, endian:EndianType):
        """Init.

        Args:
            game: the game this is for.
            address: the memory address this location lives at
            length: the length of the data in memory
            region: the region of memory this is in
            endian: Endianness of memory
        """
        super().__init__(game)
        self.ram:MemoryEntry = MemoryEntry(address, length, region, endian)