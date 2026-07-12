from aphelpers import *
from bhhelpers import *
from enum import IntEnum
from collections import namedtuple
from collections import OrderedDict
from collections.abc import Iterator
from typing import Any

# TODO: Gem thresholds

# type aliases
Name = str
Address = int
Flag = int

# enums
class TransitionGroup(IntEnum):
    IN  = 1
    OUT = 2

# constants
NO_POINTER: int = -1
NO_ID_SET: int = -1
DEFAULT_GEM_THRESHOLDS: list[int] = [25, 50, 75, 100]

def internal_id_to_offset(internal_id: int) -> int:
    """Translates internal ID to zero-indexed offset in the overall environment"""
    homeworld_index: int = int(internal_id / 10) - 1
    homeworld_offset: int = internal_id % 10
    return (homeworld_index * 6) + homeworld_offset

class SpyroConfig():
    def __init__(self):
        self.total_gem_mult:float = 0.0
        self.max_per_env_threshold:int = 0

class SpyroEnvironment():
    def __init__(self) -> None:
        self._name: str = "YOU GOOFED, PLAYABLE ENVIRONMENT EDITION."
        self.first_char:bytes = b""
        self.has_unchecked_locations: bool = False
        self.is_accessible: bool = False
        self.id: int = -1
        self.text_offset: Address = -1
        self.regions: list[SpyroRegion] = []
        self.start_region: SpyroRegion = SpyroRegion()
        self.total_gem_mult:float = 1.0
        self.gem_thresholds:list[int] = DEFAULT_GEM_THRESHOLDS.copy()
        
        self.ap:APData = APData()
        """Represents this environment's AP information"""
        
        self.extra_ap_locs:APDataContainer = APDataContainer()
        """Represents extra AP locations belonging to this environment"""
        
        self.dragons: OrderedDict[Name, SpyroCollectible] = OrderedDict()
        """dict[Name, SpyroCollectible]"""
        
        self.eggs: OrderedDict[Name, SpyroCollectible] = OrderedDict()
        """dict[Name, SpyroCollectible]"""
        
        # extra setup we're stuck doing
        self.total_gems: int = -1
        self.gem_counter: BHMemoryEntry = BHMemoryEntry(NO_POINTER, -1)

        for threshold in DEFAULT_GEM_THRESHOLDS:
            swp:APData = APData()
            swp.add_group(f"{threshold}% Gems")
            swp.name = f"{self.name} {threshold}% Gems"
            self.extra_ap_locs.add(swp)

    @property
    def all_ap_locs(self) -> APDataContainer:
        ret = APDataContainer()
        
        ret.add(self.ap)
        ret.merge(self.extra_ap_locs)
        
        for dragon in self.dragons.values():
            ret.merge(dragon.all_ap_locs)
        for egg in self.eggs.values():
            ret.merge(egg.all_ap_locs)
        
        return ret

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, val:str):
        self._name = val
        self.ap.add_group(self._name)

    def add_dragon(self, name:str, address:Address, flag:Flag) -> None:
        if name not in self.dragons:
            swp:SpyroCollectible = SpyroCollectible()
            swp.name = name
            swp.address = BHMemoryEntry(address, 1)
            swp.flag = flag
            
            self.dragons[name] = swp            
            self.dragons[name].ap.name = f"{self.name} {swp.name}"
            self.dragons[name].ap.add_group(self.name)
            self.dragons[name].ap.add_group("Dragons")

    def add_egg(self, name:str, address:Address, flag:Flag) -> None:
        if name not in self.eggs:
            swp:SpyroCollectible = SpyroCollectible()
            swp.name = name
            swp.address = BHMemoryEntry(address, 1)
            swp.flag = flag
            
            self.eggs[name] = swp
            self.eggs[name].ap.name = f"{self.name} {swp.name}"
            self.eggs[name].ap.add_group(self.name)
            self.eggs[name].ap.add_group("Eggs")

    def to_read_list(self) -> BHMemoryEntryList:
        ret:BHMemoryEntryList = BHMemoryEntryList()
        
        ret.append(self.gem_counter)
        
        for dragon in self.dragons.values():
            ret.extend(dragon.to_read_list())
        
        for egg in self.eggs.values():
            ret.extend(egg.to_read_list())
        
        return ret
    
    def reconfigure_ap(self, config:SpyroConfig) -> None:
        self.total_gem_mult = config.total_gem_mult
        
        self.gem_thresholds = []
        for threshold in [25, 50, 75, 100]:
            if threshold < config.max_per_env_threshold:
                self.gem_thresholds.append(threshold)
        
        for egg in self.eggs.values():
            egg.reconfigure_ap(config)
        for dragon in self.dragons.values():
            dragon.reconfigure_ap(config)

class SpyroGameWorld():
    def __init__(self) -> None:
        self.hubs: OrderedDict[str, SpyroHub] = OrderedDict()
        self.extra_ap_locs: APDataContainer = APDataContainer()
        
        # extra setup
        swp:APData = APData()
        swp.name = "Defeated Gnasty Gnorc"
        swp.add_group("Goal")
        self.extra_ap_locs.add(swp)
        
        self.menu:SpyroEnvironment = SpyroEnvironment()
        self.menu.name = "Menu"
        menu_region:SpyroRegion = SpyroRegion()
        menu_region.name = "Menu"
        self.menu.regions.append(menu_region)
        self.menu.start_region = menu_region
        
        self.global_stats:SpyroEnvironment = SpyroEnvironment()
        self.global_stats.name = "Global Stats"
        global_stats_region:SpyroRegion = SpyroRegion()
        global_stats_region.name = "Global Stats"
        self.global_stats.regions.append(global_stats_region)
        self.global_stats.start_region = global_stats_region

        self.balloonist_menu:SpyroEnvironment = SpyroEnvironment()
        self.balloonist_menu.name = "Balloonist Menu"
        balloonist_menu_region:SpyroRegion = SpyroRegion()
        balloonist_menu_region.name = "Baloonist Menu"
        self.balloonist_menu.regions.append(global_stats_region)
        self.balloonist_menu.start_region = balloonist_menu_region
        
    def add_hub(self, hub:"SpyroHub"):
        if hub.name not in self.hubs:
            self.hubs[hub.name] = hub
    
    def to_read_list(self) -> BHMemoryEntryList:
        ret:BHMemoryEntryList = BHMemoryEntryList()
        
        for hub in self.hubs.values():
            ret.extend(hub.to_read_list())
        
        return ret
    
    @property
    def all_ap_locs(self) -> APDataContainer:
        ret:APDataContainer = APDataContainer()
        
        ret.merge(self.extra_ap_locs)
        
        for hub in self.hubs.values():
            ret.merge(hub.all_ap_locs)
        
        return ret

    def reconfigure_ap(self, config:SpyroConfig) -> None:
        for hub in self.hubs.values():
            hub.reconfigure_ap(config)

    def list_environments(self) -> list[SpyroEnvironment]:
        ret = []
        
        for hub in self.hubs.values():
            ret.append(hub)
            
            for level in hub.levels.values():
                ret.append(level)
        
        return ret
    
    def list_environments_by_id(self) -> list[int]:
        ret = []
        
        swp = self.list_environments()
        
        for item in swp:
            ret.append(item.id)
        
        return ret

    def list_environments_by_name(self) -> list[str]:
        ret = []
        
        swp = self.list_environments()
        
        for item in swp:
            ret.append(item.name)
        
        return ret

    def find_env_by_id(self, id:int) -> SpyroEnvironment:
        ret:SpyroEnvironment = SpyroEnvironment()
        found:bool = False
        
        swp = self.list_environments()
        
        for env in swp:
            if not found:
                if env.id == id:
                    ret = env
                    found = True
                
        return ret
    
    def find_env_by_name(self, name:str) -> SpyroEnvironment:
        ret:SpyroEnvironment = SpyroEnvironment()
        found:bool = False
        
        swp = self.list_environments()
        
        for env in swp:
            if not found:
                if env.name == name:
                    ret = env
                    found = True
                
        return ret
    
    @property
    def total_gems(self) -> int:
        """total gems, taking into account the total gem multiplier"""
        
        ret:int = 0
        
        for hub in self.hubs.values():
            ret += round(hub.total_gems * hub.total_gem_mult)
            for level in hub.levels.values():
                ret += round(level.total_gems * level.total_gem_mult)
        
        return ret
    
class SpyroHub(SpyroEnvironment):
    def __init__(self) -> None:
        super().__init__()
        
        self.balloon_addresses: tuple[Address, Address] = (-1,-1)
        self.levels: OrderedDict[str, SpyroLevel] = OrderedDict()
        self.statue_head_checks: list[Address] = []


    @property
    def all_ap_locs(self) -> APDataContainer:
        ret = APDataContainer()
        
        ret.merge(super().all_ap_locs)
        
        return ret

    def add_level(self, level:"SpyroLevel"):
        if level.name not in self.levels:
            self.levels[level.name] = level
            
    def to_read_list(self) -> BHMemoryEntryList:
        ret:BHMemoryEntryList = super().to_read_list()
        
        for level in self.levels.values():
            ret.extend(level.to_read_list())
        
        return ret
    
    def reconfigure_ap(self, config:SpyroConfig) -> None:
        super().reconfigure_ap(config)
        for level in self.levels.values():
            level.reconfigure_ap(config)

class SpyroLevel(SpyroEnvironment):
    def __init__(self) -> None:
        super().__init__()
        self.portal: SpyroPortal = SpyroPortal(NO_POINTER, self, self)
        self._vortex_moby_pointer: Address = NO_POINTER
        
    def reconfigure_ap(self, config:SpyroConfig) -> None:
        super().reconfigure_ap(config)
    

    @property
    def all_ap_locs(self) -> APDataContainer:
        ret = APDataContainer()
        
        ret.merge(super().all_ap_locs)
        
        return ret
    
    @property
    def has_vortex(self) -> bool:
        return self._vortex_moby_pointer == NO_POINTER
    
    @property
    def vortex_moby_pointer(self) -> Address:
        return self._vortex_moby_pointer
    
    @vortex_moby_pointer.setter
    def vortex_moby_pointer(self, val:Address) -> None:
        self._vortex_moby_pointer = val
        if self.vortex_moby_pointer != NO_POINTER:
            swp:APData = APData()
            swp.name = f"{self.name} Vortex"
            self.extra_ap_locs.add(swp)

class SpyroCollectible():
    def __init__(self) -> None:
        self.name:str = "YOU DONE GOOFED - COLLECTIBLE EDITION"
        self.address:BHMemoryEntry = BHMemoryEntry(NO_POINTER, -1)
        self.ap: APData = APData()
        self.flag:Flag = NO_POINTER
        
    def to_read_list(self) -> BHMemoryEntryList:
        ret:BHMemoryEntryList = BHMemoryEntryList()
        
        ret.append(self.address)
        
        return ret

    @property
    def all_ap_locs(self) -> APDataContainer:
        ret = APDataContainer()
        
        ret.add(self.ap)
        
        return ret

    def reconfigure_ap(self, config:SpyroConfig) -> None:
        pass

class SpyroRegion():
    def __init__(self):
        self.name = "Invalid name"
        # TODO: add access rule to region
        # TODO: Add location list to region
        self.next:list[SpyroRegion] = []
        
    @property
    def has_next(self):
        return len(self.next) == 0

class SpyroPortal():
    def __init__(self, destination_address:Address, vanilla_destination:SpyroLevel, current_destination:SpyroLevel):
        self._destination_address:Address = NO_POINTER
        """Pointer to where what stage this goes to is stored."""
        self.vanilla_destination:SpyroLevel = vanilla_destination
        self.current_destination:SpyroLevel = current_destination
        self._portal_surface:Address = NO_POINTER
        self.destination_address = destination_address
        
    @property
    def destination_address(self) -> Address:
        return self._destination_address
    
    @destination_address.setter
    def destination_address(self, val:Address):
        self._destination_address = val
        self._portal_surface = val - 4
    
    @property
    def portal_surface(self) -> Address:
        return self._portal_surface

class RAM:
    """A handy collection of memory values and addresses for Spyro"""

    VANILLA_TOTAL_TREASURE: int = 14000  # Handy constant for doing calcs elsewhere
    UNUSED_SPACE: Address = 0x0f000  # At least, it seems unused. Test...
    FAKE_TIMER: Address = UNUSED_SPACE + 12
    LAST_SELECTED_VALID_CHOICE: Address = UNUSED_SPACE + 16
    NESTOR_UNSKIPPABLE: Address = 0x1747f4
    TUCO_EGG_MINIMUM: Address = 0x8492c
    SHOW_ON_INVENTORY_ARRAY: Address = 0x78e78

    memory_list:BHMemoryEntryList = BHMemoryEntryList()
    """List containing all the dangling memory entries"""
    
    spyro_color: BHMemoryEntry = BHMemoryEntry(0x78a80, 4)
    memory_list.append(spyro_color)
    
    # Struct:  AABBGGRR
    # default: 00000000
    # blue:    E0DD822A
    # green:   ??328600
    # yellow:  ??
    

    @classmethod
    def to_read_list(cls) -> BHMemoryEntryList:
        # oh boy
        ret:BHMemoryEntryList = BHMemoryEntryList()
        
        # start at the easiest
        ret.extend(cls.memory_list)
        
        # ask world for the rest
        ret.extend(cls.world.to_read_list())
        
        # done
        return ret

    @classmethod
    def create_ap_location_groups(cls) -> APLocationGroups:
        return cls.world.all_ap_locs.to_ap_group_list()
    
    @classmethod
    def create_ap_location_list(cls) -> APLocationList:
        return cls.world.all_ap_locs.to_ap_location_list()
    
    @classmethod
    def reconfigure_ap(cls, total_gem_mult:float, max_per_env_threshold:int) -> None:
        config:SpyroConfig = SpyroConfig()
        config.total_gem_mult = total_gem_mult
        config.max_per_env_threshold = max_per_env_threshold
        cls.world.reconfigure_ap(config)

def menu_lookup(current_world_num: int, menu_choice: int) -> int:
    """Replicates the same math the game uses for mapping a menu choice to the homeworld destination

    Args:
        current_world_num: The index of the current homeworld
        menu_choice: The current position of the menu cursor

    Returns:
        The index of the selected homeworld, or -1 if Stay Here is selected
    """
    if menu_choice > current_world_num:
        return menu_choice
    return menu_choice - 1

# force a location renumbering because AP is dumb
locations:APDataContainer = RAM.world.all_ap_locs
locations.renumber()