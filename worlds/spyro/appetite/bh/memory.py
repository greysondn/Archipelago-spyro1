"""
Module for things specific to memory access and data retention in Bizhawk, as
relates to AP.
"""

from appetite.bh.core import (
    EndianType,
    MemoryAddress,
)

class MemoryEntry():
    """Internal representation of a single memory entry from Bizhawk.
    
    Comparable, in some ways, to a RAM watch's output in Bizhawk.
    """
    def __init__(self, address:int, length:int, region:str, endian:EndianType):
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
        self.endian:EndianType = endian
    
    def __int__(self) -> int:
        """Enables int(self) to happen, for coercing this to an integer"""
        return int.from_bytes(self.raw_data, self.endian)

class MemoryEntryList(list):
    def __init__(self):
        """Init.
        """
        super().__init__()
    
    def to_batched_read_list(self) -> list[MemoryAddress]:
        """Convert this to a list for batched reads in bizhawk.

        Returns:
            List prepared for direct handing to bizhawk.
        """
        ret:list[MemoryAddress] = []
        
        for item in self:
            ret.append((item.address, item.length, item.region))

        return ret