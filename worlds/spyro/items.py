from typing import TYPE_CHECKING
try:
    from typing import final
except ImportError:
    if TYPE_CHECKING:
        from typing import final
    else:
        from typing_extensions import final

from BaseClasses import Item
from .addresses import RAM

BASE_SPYRO_ITEM_ID: int = 1000


@final
class SpyroItem(Item):
    game: str = "Spyro the Dragon"


homeworld_access: list[str] = []
level_access: list[str] = []

for hub in RAM.hub_environments:
    if hub.name != "Gnasty's World":
        homeworld_access.append(hub.name)
    for level in hub.child_environments:
        level_access.append(level.name)

boss_items: list[str] = [

]

goal_item: list[str] = ["Victory"]

# TODO: useful items: progressive Sparx?

full_item_list: list[str] = homeworld_access + level_access + boss_items + goal_item
full_item_list += trap_items + filler_items
item_id_to_name: dict[int, str] = dict(enumerate(full_item_list, start=BASE_SPYRO_ITEM_ID))
item_name_to_id: dict[str, int] = {v: k for k, v in item_id_to_name.items()}

grouped_items: dict[str, set[str]] = {
    "worlds": set(homeworld_access),
    "boss items": set(boss_items),
    "levels": set(level_access),
    "traps": set(trap_items),
    "filler": set(filler_items)
}
