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
    vortex_moby_address:Optional[int]
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

def extra_error(txt:str):
    print(f"\033[91mERROR\033[0m : {txt}\n")

def extra_error_rule(rule:int, location:str, info:str):
    extra_error(f"SPYRO R{rule:03d} VIOLATED AT: {location}\n{info}")

def extra_warning(txt:str):
    print(f"\033[93mWARNING\033[0m : {txt}\n")

def extra_utility_unimplemented(utility:int):
    extra_warning(f"SPYRO U{utility:03d} IS UNIMPLEMENTED")

def extra_warning_unimplemented(rule:int):
    extra_warning(f"SPYRO R{rule:03d} IS UNIMPLEMENTED")

def extra(data) -> tuple[bool, int]:
    ret_bool = True
    ret_int  = 0
    
    # rule 1   - hubs and levels must have counique names
    # 
    # Reason:
    # unknown. Presumably for confusion reasons?
    r1_set = set[str]()
    
    for hub in data["hubs"]:
        if hub["name"] in r1_set:
            ret_bool = False
            ret_int = ret_int + 1
            print(f"R01 violated: {hub["name"]}")
        r1_set.add(hub["name"])
        
        for level in hub["levels"]:
            if level["name"] in r1_set:
                ret_bool = False
                ret_int = ret_int + 1
                print(f"R01 violated: {level["name"]}")
            r1_set.add(level["name"])
    
    # rule 2   - categories for items must all be legal
    # 
    # Reason:
    # There are specific categories in archipelago.
    # We should only use those categories.
    # print("R02 - removed because pydantic handles it")
    
    # rule 3   - entrance_rando - mappings must show up in groups in correct groups
    #
    # Reason:
    # Entrance rando is a pain. Mapping things correctly from the getgo assures
    # us that we've not gone off the rails. Entrances are entrances; exits are
    # exits.
    r3_entrances = data["world"]["entrance_rando"]["groups"]["entrances"]
    r3_exits     = data["world"]["entrance_rando"]["groups"]["exits"]

    for preset in data["world"]["entrance_rando"]["presets"]:
        for mapping in preset["mappings"]:
            if mapping["entrance"] not in r3_entrances:
                ret_bool = False
                ret_int = ret_int + 1
                extra_error_rule(3, mapping["entrance"], "mappings must show up in correct groups")
            for exit in mapping["exits"]:
                if exit not in r3_exits:
                    ret_bool = False
                    ret_int = ret_int + 1
                    extra_error_rule(3, mapping["exit"], "mappings must show up in correct groups")
    
    # rule 4   - every region must have a unique name
    #
    # Reason:
    # This is an archipelago restriction. But even then, it'd be impossible to
    # deterministically form region to region connections without this anyway.
    r4_regions:set[str] = set()
    
    for hub in data["hubs"]:
        for region in hub["regions"]:
            if region["name"] in r4_regions:
                ret_bool = False
                ret_int = ret_int + 1
                extra_error_rule(4, region["name"], "every region must have a unique name")
            r4_regions.add(region["name"])
            
        for level in hub["levels"]:
            for region in level["regions"]:
                if region["name"] in r4_regions:
                    ret_bool = False
                    ret_int = ret_int + 1
                    extra_error_rule(4, region["name"], "every region must have a unique name")
                r4_regions.add(region["name"])
    
    # rule 5   - every location must have a unique name
    #
    # Reason
    # Archipelago restriction again. But this is also necessary to neatly map
    # items to locations in the randomizer.
    r5_locations:set[str] = set()
    
    for hub in data["hubs"]:
        for region in hub["regions"]:
            for location in region["locations"]:
                if location["name"] in r5_locations:
                    ret_bool = False
                    ret_int = ret_int + 1
                    extra_error_rule(5, location["name"], "every location must have a unique name")
            r5_locations.add(location["name"])
            
        for level in hub["levels"]:
            for region in level["regions"]:
                for location in region["locations"]:
                    if location["name"] in r5_locations:
                        ret_bool = False
                        ret_int = ret_int + 1
                        extra_error_rule(5, location["name"], "every location must have a unique name")
                    r5_locations.add(location["name"])
                
    # rule 6   - region transitions must have legal groups
    #
    # reason:
    # This is literally what make
    # s entrance rando work
    extra_warning_unimplemented(6)
    
    # rule 7   - items must have unique names
    #
    # reason:
    # Duplicates should be a count of the item, not another item.
    r7_items:set[str] = set()
    
    for item in data["world"]["items"]:
        if item["name"] in r7_items:
            ret_bool = False
            ret_int = ret_int + 1
            extra_error_rule(7, item["name"], "every item must have a unique name")
        r7_items.add(item["name"])
    
    # rule 8   - locations can only be both
    #
    # reason:
    # read is straightforward - to check the locaton.
    # write is for collect/release to work later on.
    for hub in data["hubs"]:
        for region in hub["regions"]:
            for location in region["locations"]:
                if location["bizhawk"]["io"] != "both":
                    ret_bool = False
                    ret_int = ret_int + 1
                    extra_error_rule(8, location["name"], "location io must be 'both'")
            
        for level in hub["levels"]:
            for region in level["regions"]:
                for location in region["locations"]:
                    if location["bizhawk"]["io"] != "both":
                        ret_bool = False
                        ret_int = ret_int + 1
                        extra_error_rule(8, location["name"], "location io must be 'both'")
    
    # rule 9   - items can only be write
    #
    # reason:
    # There is no situation in which ownership of an item needs read anywhere
    # but the archipelago server. So we only write to it anyway.
    extra_warning_unimplemented(9)
    
    # rule 10  - balloonist can only be write
    #
    # reason:
    # We don't actually care what is in the baloonist menu. We just rewrite the
    # whole thing.
    extra_warning_unimplemented(10)
    
    # rule 11  - hub and level ids must be unique 
    #
    # reason:
    # These map to the underlaying data. The underlying data is also unique.
    # More of a sanity check than anything.
    extra_warning_unimplemented(11)
    
    # rule 12  - text offset is write only
    #
    # reason:
    # We only ever write to the text offset. We already know what it says.
    extra_warning_unimplemented(12)
    
    # rule 13  - gem counter is read only
    #
    # reason:
    # No, we won't be giving the player one gem at a time as a collectible from
    # the multiworld, omfg.
    extra_warning_unimplemented(13)
    
    # rule 14  - vortex_moby_pointer is read only
    #
    # reason:
    # this was removed because the moby pointer is a value, not an address like
    # you'd go and read. Originally the assumption was that we'd only read that
    # address, but that's not how that works so... yeet.
    # print("R14 - removed for incorrect assumptions")
    
    # rule 15  - portal is write only
    #
    # reason:
    # We already know where vanilla portals go. We write to them to make
    # entrance randomization and the locks for level-entrance items work.
    extra_warning_unimplemented(15)
    
    # rule 16  - statue head checks are write only
    #
    # reason:
    # Long story short, the state doesn't matter, we want them open all the
    # time.
    extra_warning_unimplemented(16)
    
    # rule 17  - memory domains must be legal
    #
    # reason:
    # Making bizhawk choke is not, in fact, a good thing.
    # TODO: See if pydantic already does this for us.
    extra_warning_unimplemented(17)
    
    # rule 18 - locations are named "environment - location"
    #
    # reason:
    # consistency, and the fact I kept screwing it up when I was typing them in.
    for hub in data["hubs"]:
        for region in hub["regions"]:
            for location in region["locations"]:
                splts = location["name"].split(" - ")
                if (len(splts) < 2) or (splts[0] != hub["name"]):
                    ret_bool = False
                    ret_int = ret_int + 1
                    extra_error_rule(18, location["name"], "location name must be 'environment - location'")
                
        for level in hub["levels"]:
            for region in level["regions"]:
                for location in region["locations"]:
                    splts = location["name"].split(" - ")
                    if (len(splts) < 2) or (splts[0] != level["name"]):
                        ret_bool = False
                        ret_int = ret_int + 1
                        extra_error_rule(18, location["name"], "location name must be 'environment - location'")
    
    # rule 19 - Text offset initial character should match initial character of
    #           base title.
    #
    # reason:
    # This is aggressively written to. It should be done cleanly -
    # no change until we willfully make one.
    extra_warning_unimplemented(19)
    
    
    # utility 1 - output all location groups
    #
    # reason:
    # Getting eyes on it helps, and it also helps to make sure there's not a
    # typo somewhere.
    extra_utility_unimplemented(1)
    
    # utility 2 - output all item groups
    #
    # reason:
    # Getting eyes on it helps, and also helps us understand how we've
    # structured this in practice to make sure it's right. 
    extra_utility_unimplemented(2)
    
    return (ret_bool, ret_int)
    
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
        print("first pydantic  error again")
        errs[0].print()
        
    pydantic_errs = len(errs)
    
    print("")
    print("")
    
    extra_errs = extra(data)
    
    had_errors = ((pydantic_errs > 0) or (not extra_errs[0]))
    
    if had_errors:
        print("\033[91mERRORS FOUND\033[0m")
        print(f"{pydantic_errs + extra_errs[1]}")
    else:
        print("\033[92mNO ERRORS! WAY TO GO!\033[0m")
    
def main():
    parser = argparse.ArgumentParser(description="simple validator for data.yaml")
    parser.add_argument("path", help="path to data.yaml")
    args = parser.parse_args()
    
    with open(args.path) as f:
        data = yaml.load(f, yaml.loader.FullLoader)

    validate(data)

if __name__ == "__main__":
    main()