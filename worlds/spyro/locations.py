from BaseClasses import Location

from .addresses import RAM
from aphelpers import APLocationList, APLocationGroups, APDataContainer

class SpyroLocation(Location):
    game: str = "Spyro the Dragon"

class SpyroPlayerLocations():
    """Defines locations for a single player
    """

    def __init__(self, total_gem_mult: float, max_per_env_threshold: int) -> None:
        """Defines locations after logic changes due to options"""
        self.included_locations:set[str] = set()
        
        RAM.reconfigure_ap(total_gem_mult, max_per_env_threshold)
        
        swp:APDataContainer = RAM.world.all_ap_locs.get_active()
        
        for location in swp:
            self.included_locations.add(location.name)
        
        return


static_locations: APLocationList = RAM.create_ap_location_list()
static_loc_groups: APLocationGroups = RAM.create_ap_location_groups()