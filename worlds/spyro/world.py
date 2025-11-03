from logging import warning

from typing import TYPE_CHECKING
try:
    from typing import override, ClassVar, TypedDict
except ImportError:
    if TYPE_CHECKING:
        from typing import override, ClassVar, TypedDict
    else:
        from typing_extensions import override, ClassVar, TypedDict

from BaseClasses import Entrance, MultiWorld, Region
from BaseClasses import ItemClassification
from BaseClasses import Location
from Options import OptionError
from entrance_rando import ERPlacementState, randomize_entrances
from ..AutoWorld import WebWorld, World
from .web import SpyroWeb
from .items import SpyroItem, filler_items, goal_item
from .items import homeworld_access, level_access, boss_items, trap_items
from .items import grouped_items, item_name_to_id
from .locations import static_locations, static_loc_groups, SpyroPlayerLocations
from .options import SpyroOptions
from .regions import create_regions, ENTRANCE_OUT, ENTRANCE_IN
from .rules import set_rules
from .addresses import RAM, Environment

class SlotDataTypes(TypedDict):
    goal: str
    starting_world: int
    portal_shuffle: int
    entrances: list[tuple[str, str]]
    spyro_color: int
    global_gem_percent: int
    max_per_env_threshold: int


class SpyroWorld(World):
    """
    Spyro the Dragon, originally released on the PS1 in 1998, is a 3D collectathon platform starring the titular
    purple dragon, Spyro. Charge, jump, flame, and glide your way through 29 different levels across 6 different
    homeworlds, as you collect gems, recover stolen dragon eggs, free crystallized dragons, and make your way
    to Gnorc Gnexus to torch Gnasty and save the world of dragons.
    """
    game: ClassVar[str] = "Spyro the Dragon"
    web: ClassVar[WebWorld] = SpyroWeb()
    options_dataclass: ClassVar[type[SpyroOptions]] = SpyroOptions  # pyright: ignore[reportIncompatibleVariableOverride]
    # Following ignore is for https://github.com/python/typing/discussions/1486 reasons
    # Hopefully, eventually this becomes unnecessary
    options: SpyroOptions  # pyright: ignore[reportIncompatibleVariableOverride]
    topology_present: bool = True

    item_name_to_id: ClassVar[dict[str, int]] = item_name_to_id
    location_name_to_id: ClassVar[dict[str, int]] = static_locations

    item_name_groups: ClassVar[dict[str, set[str]]] = grouped_items
    location_name_groups: ClassVar[dict[str, set[str]]] = static_loc_groups

    player_locations: SpyroPlayerLocations | None = None

    _goal: str
    _portal_shuffle: int
    _death_link: int
    _starting_world: int
    _spyro_color: int
    _gem_threshold_mult: float
    _per_env_threshold: int

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self._goal = "gnasty"
        self._portal_shuffle = 0
        self._death_link = 0
        self._starting_world = 0
        self._spyro_color = -1
        self._gem_threshold_mult = 1.0
        self._per_env_threshold = 100
        self.shuffled_entrance_pairings: list[tuple[str, str]] = []
        self.env_by_id: dict[int, Environment] = {}
        self.env_by_name: dict[str, Environment] = {}

        for hub in RAM.hub_environments:
            self.env_by_id[hub.internal_id] = hub
            self.env_by_name[hub.name] = hub

            for level in hub.child_environments:
                self.env_by_id[level.internal_id] = level
                self.env_by_name[level.name] = level

    @property
    def goal(self) -> str:
        """Goal for this world

        Returns:
            The goal name
        """
        return self._goal

    @goal.setter
    def goal(self, value: str) -> None:
        if value in ("gnasty", "loot"):
            self._goal = value
        else:
            raise OptionError(f"Invalid value {value} for goal for player {self.player_name}")

        return

    @property
    def portal_shuffle(self) -> bool:
        """Whether portals are shuffled

        Returns:
            bool
        """
        return self._portal_shuffle == 1

    @portal_shuffle.setter
    def portal_shuffle(self, value: bool) -> None:
        if value:
            self._portal_shuffle = 1
        else:
            self._portal_shuffle = 0

        return

    @property
    def death_link(self) -> bool:
        """Whether death link is on

        Returns:
            bool
        """
        return self._death_link == 1

    @death_link.setter
    def death_link(self, value: bool) -> None:
        if value:
            warning(f"Deathlink for {self.game} doesn't work yet. Option will be ignored.")
            self._death_link = 1
        else:
            self._death_link = 0

        return

    @property
    def starting_world(self) -> int:
        """Which world the player starts in

        Returns:
            The index of the homeworld
        """
        return self._starting_world

    @starting_world.setter
    def starting_world(self, value: int) -> None:
        if value in range(5):
            self._starting_world = value
        else:
            raise OptionError(
                "This shouldn't happen! Let the dev of the apworld for " +
                f"{self.game} know that starting_homeworld broke!"
            )

        return

    @property
    def spyro_color(self) -> int:
        """Spyro's RGBA color"""
        return self._spyro_color

    @spyro_color.setter
    def spyro_color(self, value: str) -> None:
        try:
            color: int = int(value, 16)
        except ValueError as exc:
            raise OptionError(
                f"{self.player_name}'s spyro_color value of " + f'"{value}" is not a valid RGBA color.'
            ) from exc
        self._spyro_color = color

        return

    @property
    def gem_threshold_mult(self) -> float:
        """Multiplier for total gem threshold locations

        Returns:
            float
        """
        return self._gem_threshold_mult

    @gem_threshold_mult.setter
    def gem_threshold_mult(self, value: float) -> None:
        if (value >= 0.01) and (value <= 1.0):
            self._gem_threshold_mult = value
        else:
            raise OptionError(
                f"Somehow, {self.player} managed to break their yaml with the global_gem_percent option "
                + f"with a value of {int(value)}."
            )

        return

    @property
    def per_env_max_gem_threshold(self) -> int:
        """Max percentage threshold for per-area gem locations.

        Returns:
            int
        """
        return self._per_env_threshold

    @per_env_max_gem_threshold.setter
    def per_env_max_gem_threshold(self, amount: int) -> None:
        if amount % 25 == 0:
            self._per_env_threshold = amount
        else:
            raise OptionError(f"Invalid value {amount} for option max_level_gem_threshold for player {self.player}")

    @override
    def generate_early(self) -> None:
        self.goal = self.options.goal.get_option_name(self.options.goal.value).lower()
        self.starting_world = self.options.starting_world.value
        if self.options.spyro_color.value == "random":
            random_rgb: bytes = self.random.randbytes(3)
            temp_color: str = random_rgb.hex() + "ff"  # Ensure full alpha
            self.spyro_color = temp_color
        else:
            self.spyro_color = self.options.spyro_color.value
        self.death_link = self.options.death_link.value == 1
        self.portal_shuffle = self.options.portal_shuffle.value == 1
        self.gem_threshold_mult = self.options.global_gem_percent.value / 100.0
        self.per_env_max_gem_threshold = self.options.max_level_gem_threshold.value

        self.player_locations = SpyroPlayerLocations(
            list(self.env_by_id.values()),
            self.gem_threshold_mult,
            self.per_env_max_gem_threshold,
        )

        return

    @override
    def create_regions(self) -> None:
        if (self.player_locations is not None) and (not hasattr(self.multiworld, "generation_is_fake")):
            create_regions(self, self.starting_world, self.player_locations)

        return

    @override
    def create_item(self, name: str) -> SpyroItem:
        classification: ItemClassification
        if name in filler_items:
            classification = ItemClassification.filler
        elif name in trap_items:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.progression

        return SpyroItem(name, classification, self.item_name_to_id[name], self.player)

    @override
    def create_items(self) -> None:
        """Mutate the multiworld itempool to include items for Spyro.
        """
        itempool: list[SpyroItem] = []
        for name in homeworld_access:
            if name == RAM.hub_environments[self.starting_world].name:
                self.push_precollected(self.create_item(name))
            else:
                itempool += [self.create_item(name)]

        for name in level_access:
            itempool += [self.create_item(name)]

        for name in boss_items:
            itempool += [self.create_item(name)]

        victory: SpyroItem = self.create_item(goal_item[0])

        trap_percentage: float = 0.05
        total_unfilled_locations: int = len(self.multiworld.get_unfilled_locations(self.player))

        # Ensure we're not in UT gen, because we can't look up these by name until later
        if not hasattr(self.multiworld, "generation_is_fake"):
            if self.goal == "gnasty":
                self.get_location("Defeated Gnasty Gnorc").place_locked_item(victory)
            elif self.goal == "loot":
                self.get_location("Gnasty's Loot Vortex").place_locked_item(victory)
        
            total_unfilled_locations -= 1
        
        total_filled_local_locations: int = len(itempool)
        trap_count: int = round((total_unfilled_locations - total_filled_local_locations) * trap_percentage)
        total_filled_local_locations += trap_count

        for _ in range(trap_count):
            random_trap: str = self.multiworld.random.choice(trap_items)
            itempool += [self.create_item(random_trap)]

        junk_count: int = total_unfilled_locations - total_filled_local_locations

        for _ in range(junk_count):
            random_filler: str = self.multiworld.random.choice(filler_items)
            itempool += [self.create_item(random_filler)]

        self.multiworld.itempool += itempool

    @override
    def connect_entrances(self) -> None:
        if not hasattr(self.multiworld, "generation_is_fake"):  # If not in UT gen, do the rest
            if self.portal_shuffle:
                # Ensure vanilla connection on goal level
                goal_level: str = ""
                if self.goal == "gnasty":
                    goal_level = "Gnasty Gnorc"
                elif self.goal == "loot":
                    goal_level = "Gnasty's Loot"

                gnasty_hub: Region = self.get_region("Gnasty's World")
                goal_level_region: Region = self.get_region(goal_level)

                dangling_entrance_hub: Entrance = Entrance(self.player, "")
                dangling_entrance_level: Entrance = Entrance(self.player, "")
                dangling_exit_hub: Entrance = Entrance(self.player, "")
                dangling_exit_level: Entrance = Entrance(self.player, "")

                first_unshuffled_pairing: list[str] = ["", ""]
                second_unshuffled_pairing: list[str] = ["", ""]

                # Iterate through hub and level's exits to grab pair of dangling exits, and save names to add to
                # slot data for later, so the client can lookup the vanilla connection without special casing
                for named_exit in gnasty_hub.exits:
                    if goal_level in named_exit.name:
                        dangling_exit_hub = named_exit
                        first_unshuffled_pairing[0] = named_exit.name
                        second_unshuffled_pairing[1] = named_exit.name
                for named_exit in goal_level_region.exits:
                    if goal_level in named_exit.name:
                        dangling_exit_level = named_exit
                        first_unshuffled_pairing[1] = named_exit.name
                        second_unshuffled_pairing[0] = named_exit.name

                # Iterate through hub and level's entrances to grab pair of dangling entrances
                for entrance in gnasty_hub.entrances:
                    if goal_level in entrance.name:
                        dangling_entrance_hub = entrance
                for entrance in goal_level_region.entrances:
                    if goal_level in entrance.name:
                        dangling_entrance_level = entrance

                # Actually connect the two pairs. Generic ER is confusing
                dangling_entrance_hub.parent_region = dangling_exit_level.parent_region
                dangling_entrance_level.parent_region = dangling_exit_hub.parent_region
                dangling_exit_hub.connected_region = dangling_entrance_level.connected_region
                dangling_exit_level.connected_region = dangling_entrance_hub.connected_region

                # Create shuffled connections with GER call
                shuffled_entrances: ERPlacementState = randomize_entrances(
                    self,
                    True,
                    {
                        ENTRANCE_IN: [ENTRANCE_OUT],
                        ENTRANCE_OUT: [ENTRANCE_IN]
                    },
                    False
                )

                # Save results for filling slot data later
                self.shuffled_entrance_pairings = shuffled_entrances.pairings

                # Tack on vanilla goal level pairings to slot data
                self.shuffled_entrance_pairings.append((first_unshuffled_pairing[0], first_unshuffled_pairing[1]))
                self.shuffled_entrance_pairings.append((second_unshuffled_pairing[0], second_unshuffled_pairing[1]))

            else:
                all_ents_list: list[Entrance] = []

                for entrance in self.get_entrances():
                    all_ents_list.append(entrance)

                levels_start: int = 0
                levels_stop: int = 0

                for index, ent in enumerate(all_ents_list):
                    if ("Stone Hill" in ent.name) and (levels_start == 0):
                        levels_start = index
                    elif "Gnasty's Loot" in ent.name:
                        levels_stop = index

                vanilla_pairs: list[tuple[Entrance, Entrance]] = []

                for index in range(levels_start, levels_stop, 2):
                    vanilla_pairs.append((all_ents_list[index], all_ents_list[index + 1]))

                for pair in vanilla_pairs:
                    if (
                        (pair[0].parent_region is not None)
                        and (pair[1].parent_region is not None)
                        and (pair[0].connected_region is None)
                        and (pair[1].connected_region is None)
                    ):
                        pair[0].connect(pair[1].parent_region)
                        pair[1].connect(pair[0].parent_region)

    @override
    def set_rules(self) -> None:
        if not hasattr(self.multiworld, "generation_is_fake"):
            set_rules(self, self.gem_threshold_mult, list(self.env_by_id.values()))

    @override
    def fill_slot_data(self) -> dict[str, int | list[tuple[str, str]] | str]:
        return {
            "goal": self.goal,
            "starting_world": self.starting_world,
            "portal_shuffle": 1 if self.portal_shuffle else 0,
            "entrances": self.shuffled_entrance_pairings,
            "spyro_color": self.spyro_color,
            "global_gem_percent": int(self.gem_threshold_mult * 100.0),
            "max_per_env_threshold": self.per_env_max_gem_threshold
        }

    @override
    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        """Given hint_data from the multiworld, mutate it to modify the entrance data, which is used in the hints tab.

        Args:
            hint_data: Archipelago's hint_data, indexed by player and location ID
        """
        hint_data.update({self.player: {}})  # Taken from Tunic. Not sure why this is needed. Doesn't work without.
        new_hint_data: dict[int, dict[int, str]] = hint_data
        if self.portal_shuffle:
            # Iterate locations for mapping their entrances as needed
            for name, loc_id in self.location_name_to_id.items():
                if (self.player_locations is not None) and (name in self.player_locations.included_locations):
                    location: Location = self.multiworld.get_location(name, self.player)
                    region_name: str = "No level should match this substring"

                    if location.parent_region is not None:
                        region_name = location.parent_region.name

                    if (region_name in self.env_by_name) and (not self.env_by_name[region_name].is_hub()):
                        new_hint_data[self.player][loc_id] = self.lookup_shuffled_entrance(region_name)

        hint_data = new_hint_data
        return

    def lookup_shuffled_entrance(self, level_name: str) -> str:
        """Given the name of a level, find the name of the portal that leads to it

        Args:
            level_name: The name of the level to find the entrance for

        Returns:
            The name of the portal that leads to the given level
        """
        entrance_portal_name: str = ""
        unstripped_portal_name: str = ""

        # Find the mapped fly-in to the given level, save the mapped portal for later
        for pairing in self.shuffled_entrance_pairings:
            if (level_name in pairing[0]) and ("Fly-in" in pairing[0]):
                unstripped_portal_name = pairing[1]

        # Find the level that matches the portal name from earlier, save for returning
        for env_name in self.env_by_name:
            if env_name in unstripped_portal_name:
                entrance_portal_name = env_name

        return entrance_portal_name

    def interpret_slot_data(self, slot_data: SlotDataTypes) -> None:
        """Method called by UT, where we can handle deferred logic stuff

        Args:
            slot_data: Holds slot data, indexed by name of the piece of data
        """
        self.starting_world = slot_data["starting_world"]
        self.gem_threshold_mult = slot_data["global_gem_percent"] / 100.0
        self.per_env_max_gem_threshold = slot_data["max_per_env_threshold"]
        self.player_locations = SpyroPlayerLocations(
            list(self.env_by_id.values()),
            self.gem_threshold_mult,
            self.per_env_max_gem_threshold,
        )
        create_regions(self, self.starting_world, self.player_locations)
        set_rules(self, self.gem_threshold_mult, list(self.env_by_id.values()))
        # Connect starting homeworld to menu region
        regions: dict[str, Region] = self.multiworld.regions.region_cache[self.player]
        entrances: dict[str, Entrance] = self.multiworld.regions.entrance_cache[self.player]

        starting_homeworld_index: int = slot_data["starting_world"]
        starting_homeworld: str = RAM.hub_environments[starting_homeworld_index].name
        starting_region: Region = regions[starting_homeworld]
        menu: Region = regions["Menu"]

        _ = menu.connect(starting_region, "Starting Homeworld")

        # Set local copy of gem threshold percentage
        self.gem_threshold_mult = slot_data["global_gem_percent"] / 100.0

        # Connect entrances
        if slot_data["portal_shuffle"] == 1:

            # Ensure vanilla connection on goal level
            goal_level: str = ""
            if slot_data["goal"] == "gnasty":
                goal_level = "Gnasty Gnorc"
            elif slot_data["goal"] == "loot":
                goal_level = "Gnasty's Loot"

            gnasty_hub = regions["Gnasty's World"]
            goal_level_region = regions[goal_level]

            dangling_entrance_hub: Entrance = Entrance(self.player, "")
            dangling_entrance_level: Entrance = Entrance(self.player, "")
            dangling_exit_hub: Entrance = Entrance(self.player, "")
            dangling_exit_level: Entrance = Entrance(self.player, "")

            # Iterate through hub and level's exits to grab pair of dangling exits
            for named_exit in gnasty_hub.exits:
                if goal_level in named_exit.name:
                    dangling_exit_hub = named_exit
            for named_exit in goal_level_region.exits:
                if goal_level in named_exit.name:
                    dangling_exit_level = named_exit

            # Iterate through hub and level's entrances to grab pair of dangling entrances
            for entrance in gnasty_hub.entrances:
                if goal_level in entrance.name:
                    dangling_entrance_hub = entrance
            for entrance in goal_level_region.entrances:
                if goal_level in entrance.name:
                    dangling_entrance_level = entrance

            # Generic ER is so confusing
            dangling_entrance_hub.parent_region = dangling_exit_level.parent_region
            dangling_entrance_level.parent_region = dangling_exit_hub.parent_region
            dangling_exit_hub.connected_region = dangling_entrance_level.connected_region
            dangling_exit_level.connected_region = dangling_entrance_hub.connected_region

            # Connect remaining ER entrances
            pairings: list[tuple[str, str]] = slot_data["entrances"]

            for pairing in pairings:
                first_entrance: Entrance = entrances[pairing[0]]
                second_entrance: Entrance = entrances[pairing[1]]
                if (first_entrance.parent_region is not None) and (second_entrance.parent_region is not None):
                    first_entrance.connect(second_entrance.parent_region)
                    second_entrance.connect(first_entrance.parent_region)
        else:
            all_entrances: dict[str, Entrance] = entrances
            all_ents_list: list[Entrance] = []

            for entrance in all_entrances.values():
                all_ents_list.append(entrance)

            levels_start: int = 0
            levels_stop: int = 0

            for index, ent in enumerate(all_ents_list):
                if ("Stone Hill" in ent.name) and (levels_start == 0):
                    levels_start = index
                elif "Gnasty's Loot" in ent.name:
                    levels_stop = index

            vanilla_pairs: list[tuple[Entrance, Entrance]] = []

            for index in range(levels_start, levels_stop, 2):
                vanilla_pairs.append((all_ents_list[index], all_ents_list[index + 1]))

            for pair in vanilla_pairs:
                if (
                    (pair[0].parent_region is not None)
                    and (pair[1].parent_region is not None)
                    and (pair[0].connected_region is None)
                    and (pair[1].connected_region is None)
                ):
                    pair[0].connect(pair[1].parent_region)
                    pair[1].connect(pair[0].parent_region)
