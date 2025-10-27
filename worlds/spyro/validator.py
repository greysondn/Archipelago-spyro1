# So, this validator requires pydantic.
# pip install pydantic
# or, if you're a good [girl/boy/etc] what never did wrong
# pipenv install pydantic
#
# We observed there was no need to make pydantic a hard requirement in the
# archipelago distribution, because it's only used as a development library.
#

import argparse
import yaml

import sys
import pprint
import textwrap

try:
    import pydantic
except ImportError:
    print("You must install pydantic to use this file!")
    print("maybe")
    print("pip install pydantic")
    print("or")
    print("pipenv install pydantic")
    print("?")
    # hard crash
    sys.exit(1)
    
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    ValidationError,
)

from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Union
)

from appetite.validate.ap.item.item import Item as ApItem
from appetite.validate.ap.rando.entrance import Entrance
from appetite.validate.bh.item import Item as BhItem
from appetite.validate.bh.data import Data as BhData
from appetite.validate.bh.region import Region as BhRegion

class SpyroWorld(BaseModel):
    items:Sequence[Union[BhItem, ApItem]]
    entrance_rando:Entrance
    
    model_config = ConfigDict(
        extra = "forbid",
    )

class SpyroLevel(BaseModel):
    name:str
    id:int
    vortex_moby_address:int
    text_offset:BhData
    total_gems:int
    gem_counter:BhData
    regions:Sequence[BhRegion]
    portal:BhData
    groups:Sequence[str]
    
    model_config = ConfigDict(
        extra = "forbid",
    )

class SpyroHub(BaseModel):
    name:str
    id:int
    balloon_addresses:Sequence[BhData]
    text_offset:BhData
    total_gems:int
    gem_counter:BhData
    regions:Sequence[BhRegion]
    levels:Sequence[SpyroLevel]
    statue_head_checks:list[BhData]
    
    model_config = ConfigDict(
        extra = "forbid",
    )

class SpyroVar(BaseModel):
    address:BhData
    values:Dict[str,Any]

class SpyroRoot(BaseModel):
    game:Literal["Spyro the Dragon"]
    vars:Dict[str, SpyroVar]
    world:SpyroWorld
    hubs:Sequence[SpyroHub]
    
    model_config = ConfigDict(
        extra = "forbid",
    )
    
def extra(data) -> bool:
    ret = True
    
    # rule 1   - hubs and levels must have counique names
    r1_set = set[str]()
    
    for hub in data["hubs"]:
        if hub["name"] in r1_set:
            ret = False
            print(f"R1 violated: {hub["name"]}")
        r1_set.add(hub["name"])
        
        for level in hub["levels"]:
            if level["name"] in r1_set:
                ret = False
                print(f"R1 violated: {level["name"]}")
            r1_set.add(level["name"])
    
    # rule 2   - categories for items must all be legal
    # ERPS THIS IS VALIDATED ALREADY
    
    # rule 3   - entrance_rando - mappings must show up in groups in correct groups
    r3_entrances = data["world"]["entrance_rando"]["groups"]["entrances"]
    r3_exits     = data["world"]["entrance_rando"]["groups"]["exits"]

    for preset in data["world"]["entrance_rando"]["presets"]:
        for mapping in preset["mappings"]:
            if mapping["entrance"] not in r3_entrances:
                ret = False
                print(f"R3 violated: {mapping["entrance"]}")
            for exit in mapping["exits"]:
                if exit not in r3_exits:
                    ret = False
                    print(f"R3 violated: {exit}")
    
    # rule 4   - every region must have a distinct name
    r4_regions:set[str] = set()
    
    for hub in data["hubs"]:
        for region in hub["regions"]:
            if region["name"] in r4_regions:
                ret = False
                print(f"R4 violated: {region["name"]}")
            r4_regions.add(region["name"])
            
        for level in hub["levels"]:
            for region in level["regions"]:
                if region["name"] in r4_regions:
                    ret = False
                    print(f"R4 violated: {region["name"]}")
                r4_regions.add(region["name"])
    
    # rule 5   - every location must have a distinct name
    print("WARNING! R5 IS UNIMPLEMENTED!")
                
    # rule 6   - region transitions must have legal groups
    print("WARNING! R6 IS UNIMPLEMENTED!")
    
    # rule 7   - items must have unique names
    print("WARNING! R7 IS UNIMPLEMENTED!")
    
    # rule 8   - locations can only be both
    print("WARNING! R8 IS UNIMPLEMENTED!")
    
    # rule 9   - items can only be write
    print("WARNING! R9 IS UNIMPLEMENTED!")
    
    # rule 10  - balloonist can only be write
    print("WARNING! R10 IS UNIMPLEMENTED!")
    
    # rule 11  - hub and level ids must be unique 
    print("WARNING! R11 IS UNIMPLEMENTED!")
    
    # rule 12  - text offset is write only
    print("WARNING! R12 IS UNIMPLEMENTED!")
    
    # rule 13  - gem counter is read only
    print("WARNING! R13 IS UNIMPLEMENTED!")
    
    # rule 14  - vortex_moby_pointer is read only
    print("WARNING! R14 IS UNIMPLEMENTED!")
    
    # rule 15  - portal is write only
    print("WARNING! R15 IS UNIMPLEMENTED!")
    
    # rule 16  - statue head checks are write only
    print("WARNING! R16 IS UNIMPLEMENTED!")
    
    # rule 17  - memory domains must be legal
    print("WARNING! R17 IS UNIMPLEMENTED!")
    
    # utility 1 - output all location groups
    print("WARNING! U1 IS UNIMPLEMENTED!")
    
    # utility 2 - output all item groups 
    print("WARNING! U2 IS UNIMPLEMENTED!")
    
    return ret
    
def validate(data):
    class _Err():
        def __init__(self, type:str, loc:Any, msg:str, val:Any):
            self.type:str = type
            self.loc = loc
            self.msg = msg
            self.val = val
        
        def try_get(self, alternated_keys:Sequence[str], final_keys:Sequence[str]=[]) -> Any:
            ret = None
            total_len = len(alternated_keys) * 2 + len(final_keys)
            
            if len(self.loc) >= total_len:
                swp = data
                legal = True
                
                for akey_id in range(len(alternated_keys)):
                    if self.loc[akey_id * 2] != alternated_keys[akey_id]:
                        legal = False
                
                for fkey_id in range(len(final_keys) - 1):
                    ind = (len(alternated_keys) * 2) + fkey_id
                    if self.loc[ind] != final_keys[fkey_id]:
                        legal = False
                
                if legal:
                    for akey_id in range(len(alternated_keys)):
                        base_id = akey_id * 2
                        swp = swp[self.loc[base_id]]
                        swp = swp[self.loc[base_id + 1]]
                    
                    for fkey in final_keys:
                        swp = swp[fkey]
                    
                    ret = str(swp)
                    
            return ret
        
        def printed_try_get(self, prefix:str, alternated_keys:Sequence[str], final_keys:Sequence[str]=[]) -> None:
            val:Any = self.try_get(alternated_keys, final_keys)
            
            if val is not None:
                print(f"{prefix} : {val}")
        
        def print(self, width:int=79, indent:int=4):
            print("-" * width)
            print("Error!")
            print(self.type)
            print("-" * width)
            
            print("")
            
            print("Message")
            for line in textwrap.wrap(self.msg, width=width):
                print(line)
            
            print("")
            
            print("Given value (may be formatted wrong)")
            pprint.pprint(self.val, indent=indent, width=width, depth=2)
            
            print("")
            
            print("Location")
            pprint.pprint(self.loc, indent=indent, width=width, depth=2)
            
            print("")
            
            print("View attempt (may be blank or incomplete)")
            self.printed_try_get("Hub Name", ["hubs"], ["name"])
            
            # directly on the hub
            self.printed_try_get("Region Name", ["hubs", "regions"], ["name"])
            self.printed_try_get("Location Name", ["hubs", "regions", "locations"], ["name"])
            
            # in a level
            self.printed_try_get("Level Name", ["hubs", "levels"], ["name"])
            self.printed_try_get("Region Name", ["hubs", "levels", "regions"], ["name"])
            self.printed_try_get("Location Name", ["hubs", "levels", "regions", "locations"], ["name"])
    errs:List[_Err] = []
    
    try:
        _ = SpyroRoot(
                vars=data["vars"],
                game=data["game"],
                world=data["world"],
                hubs=data["hubs"],
            )
    except ValidationError as e:
        for err in e.errors():
            swp:_Err = _Err(
                err["type"],
                err["loc"],
                err["msg"],
                err["input"],
            )

            errs.append(swp)

    for err in errs:
        print("")
        print("")
        err.print()
    
    if len(errs) > 0:
        print("")
        print("")
        print("first error again")
        errs[0].print()
    
    print("")
    print("")
    print("Total errors")
    print(len(errs))
    
    # extra(data)
    
def main():
    parser = argparse.ArgumentParser(description="simple validator for data.yaml")
    parser.add_argument("path", help="path to data.yaml")
    args = parser.parse_args()
    
    with open(args.path) as f:
        data = yaml.load(f, yaml.loader.FullLoader)

    validate(data)

if __name__ == "__main__":
    main()