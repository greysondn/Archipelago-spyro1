from aphelpers import APLocation
from typing import List
from typing import Literal
from typing import Tuple

BHEndianType = Literal["little", "big"]
"""String literal of data for memory"""

BHMemoryAddress = Tuple[int, int, str]
"""(address, length_in_bytes, region)"""

class BHLocation(APLocation):
    """An APLocation, with extras for Bizhawk implementations"""
    def __init__(self, game:str, address:int, length:int, region:str, endian:BHEndianType):
        """Init.

        Args:
            game: the game this is for.
            address: the memory address this location lives at
            length: the length of the data in memory
            region: the region of memory this is in
            endian: Endianness of memory
        """
        super().__init__(game)
        self.ram:BHMemoryEntry = BHMemoryEntry(address, length, region, endian)

class BHMemoryEntry():
    """Internal representation of a single memory entry from Bizhawk.
    
    Comparable, in some ways, to a RAM watch's output in Bizhawk.
    """
    def __init__(self, address:int, length:int, region:str, endian:BHEndianType):
        """Init.

        Args:
            address: where this resides in memory
            length: the length of this in memory
            region: the region of memory this is in
            endian: Endianess of this data point.
        """
        self.raw_data:bytes = b""
        self.address:int = address
        self.length:int = length
        self.region:str = region
        self.endian:BHEndianType = endian
    
    def __int__(self) -> int:
        """Enables int(self) to happen, for coercing this to an integer"""
        return int.from_bytes(self.raw_data, self.endian)

class BHMemoryEntryList(list):
    def __init__(self):
        """Init.
        """
        super().__init__()
    
    def to_batched_read_list(self) -> List[BHMemoryAddress]:
        """Convert this to a list for batched reads in bizhawk.

        Returns:
            List prepared for direct handing to bizhawk.
        """
        ret:list[BHMemoryAddress] = []
        
        for item in self:
            ret.append((item.address, item.length, item.region))

        return ret

# define everything for lazy import
__all__ = [
    "BHLocation",
    "BHMemoryEntry",
    "BHMemoryEntryList",
]