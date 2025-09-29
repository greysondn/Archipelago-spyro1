from aphelpers import APLocation

class BHLocation(APLocation):
    def __init__(self, game:str, address:int, length:int):
        super().__init__(game)
        self.ram:BHMemoryEntry = BHMemoryEntry(address, length)

class BHMemoryEntry():
    def __init__(self, address:int, length:int):
        self.raw_data:bytes = b""
        self.address:int = address
        self.length:int = length
        self.region = "MainRam"
    
    def __int__(self):
        return int.from_bytes(self.raw_data, "little")

class BHMemoryEntryList(list):
    def __init__(self):
        super().__init__()
    
    def to_batched_read_list(self) -> list[tuple[int, int, str]]:
        ret:list[tuple[int, int, str]] = []
        
        for item in self:
            ret.append((item.address, item.length, item.region))

        return ret

# define everything for lazy import
__all__ = [
    "BHLocation",
    "BHMemoryEntry",
    "BHMemoryEntryList",
]