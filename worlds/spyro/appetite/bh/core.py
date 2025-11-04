"""
Module for stuff specific to core AP Bizhawk implementations
"""

from typing import (
    Literal,
    Tuple,
)

# ------------
# type aliases
# ------------

EndianType = Literal["little", "big"]
"""String literal of data for memory"""

MemoryAddress = Tuple[int, int, str]
"""(address:int, length_in_bytes:int, region:str)"""