from aphelpers import APLocation
from typing import List
from typing import Tuple

BHMemoryAddress = Tuple[int, int, str]
"""(address, length_in_bytes, region)"""

class BHLocation(APLocation):
    def __init__(self, game:str, address:int, length:int):
        super().__init__(game)
        self.ram:BHMemoryEntry = BHMemoryEntry(address, length)

class BHMemoryEntry():
    def __init__(self, address:int, length:int):
        self.raw_data:bytes = b""
        self.address:int = address
        self.length:int = length
        self.region:str = "MainRam"
    
    def __int__(self) -> int:
        return int.from_bytes(self.raw_data, "little")

class BHMemoryEntryList(list):
    def __init__(self):
        super().__init__()
    
    def to_batched_read_list(self) -> List[BHMemoryAddress]:
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