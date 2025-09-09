from enum import IntEnum


def internal_id_to_offset(internal_id: int) -> int:
    """Translates internal ID to zero-indexed offset in the overall environment"""
    homeworld_index: int = int(internal_id / 10) - 1
    homeworld_offset: int = internal_id % 10
    return (homeworld_index * 6) + homeworld_offset

class SpyroEnvironment():
    """A container holding various useful pieces of data tied to a given level or homeworld"""
    balloon_pointers: list[int]
    name: str
    internal_id: int
    text_offset: int
    has_vortex: bool

    dragons: dict[str, tuple[int, int]]
    """dragons[name] = (address, flag)"""

    eggs: dict[str, tuple[int, int]]
    """eggs[name] = (address, flag)"""

    gem_counter: int
    total_gems: int
    statue_head_checks: list[int]
    child_environments: list["SpyroEnvironment"]
    portal_surface_types: list[int]
    portal_dest_level_ids: list[int]
    vortex_moby_pointer: int

    def __init__(self, name: str, internal_id: int, has_vortex: bool = False) -> None:
        self.name = name
        self.internal_id = internal_id
        self.balloon_pointers = []
        self.text_offset = 0
        self.has_vortex = has_vortex
        self.dragons = {}
        self.eggs = {}
        self.gem_counter = 0
        self.total_gems = 0
        self.statue_head_checks = []
        self.child_environments = []
        self.portal_surface_types = []
        self.portal_dest_level_ids = []
        self.vortex_moby_pointer = 0

    def is_hub(self) -> bool:
        """Whether the current environment is a homeworld"""
        is_hub: bool = False
        if self.internal_id % 10 == 0:
            is_hub = True
        return is_hub


class RAM:
    """A handy collection of memory values and addresses for Spyro"""

    TOTAL_TREASURE: int = 14000  # Handy constant for doing calcs elsewhere

    unused_space: int = 0x0f000  # At least, it seems unused. Test...

    last_received_archipelago_id: int = unused_space + 4
    """The ID of the last item the game has been given. Useful for save state issues and such."""

    switched_portal_dest: int = unused_space + 8

    fake_timer: int = unused_space + 12

    last_selected_valid_choice: int = unused_space + 16

    hub_environments: list[SpyroEnvironment] = []

    hub_environments.append(SpyroEnvironment("Artisans", 10))
    hub_environments.append(SpyroEnvironment("Peace Keepers", 20))
    hub_environments.append(SpyroEnvironment("Magic Crafters", 30))
    hub_environments.append(SpyroEnvironment("Beast Makers", 40))
    hub_environments.append(SpyroEnvironment("Dream Weavers", 50))
    hub_environments.append(SpyroEnvironment("Gnasty's World", 60))

    hub_environments[0].child_environments.append(SpyroEnvironment("Stone Hill", 11, True))
    hub_environments[0].child_environments.append(SpyroEnvironment("Dark Hollow", 12, True))
    hub_environments[0].child_environments.append(SpyroEnvironment("Town Square", 13, True))
    hub_environments[0].child_environments.append(SpyroEnvironment("Toasty", 14, True))
    hub_environments[0].child_environments.append(SpyroEnvironment("Sunny Flight", 15))

    hub_environments[1].child_environments.append(SpyroEnvironment("Dry Canyon", 21, True))
    hub_environments[1].child_environments.append(SpyroEnvironment("Cliff Town", 22, True))
    hub_environments[1].child_environments.append(SpyroEnvironment("Ice Cavern", 23, True))
    hub_environments[1].child_environments.append(SpyroEnvironment("Doctor Shemp", 24, True))
    hub_environments[1].child_environments.append(SpyroEnvironment("Night Flight", 25))

    hub_environments[2].child_environments.append(SpyroEnvironment("Alpine Ridge", 31, True))
    hub_environments[2].child_environments.append(SpyroEnvironment("High Caves", 32, True))
    hub_environments[2].child_environments.append(SpyroEnvironment("Wizard Peak", 33, True))
    hub_environments[2].child_environments.append(SpyroEnvironment("Blowhard", 34, True))
    hub_environments[2].child_environments.append(SpyroEnvironment("Crystal Flight", 35))

    hub_environments[3].child_environments.append(SpyroEnvironment("Terrace Village", 41, True))
    hub_environments[3].child_environments.append(SpyroEnvironment("Misty Bog", 42, True))
    hub_environments[3].child_environments.append(SpyroEnvironment("Tree Tops", 43, True))
    hub_environments[3].child_environments.append(SpyroEnvironment("Metalhead", 44, True))
    hub_environments[3].child_environments.append(SpyroEnvironment("Wild Flight", 45))

    hub_environments[4].child_environments.append(SpyroEnvironment("Dark Passage", 51, True))
    hub_environments[4].child_environments.append(SpyroEnvironment("Lofty Castle", 52, True))
    hub_environments[4].child_environments.append(SpyroEnvironment("Haunted Towers", 53, True))
    hub_environments[4].child_environments.append(SpyroEnvironment("Jacques", 54, True))
    hub_environments[4].child_environments.append(SpyroEnvironment("Icy Flight", 55))

    hub_environments[5].child_environments.append(SpyroEnvironment("Gnorc Cove", 61, True))
    hub_environments[5].child_environments.append(SpyroEnvironment("Twilight Harbor", 62, True))
    hub_environments[5].child_environments.append(SpyroEnvironment("Gnasty Gnorc", 63))
    hub_environments[5].child_environments.append(SpyroEnvironment("Gnasty's Loot", 64, True))

    hub_environments[0].balloon_pointers = [0x7bc04, 0x7bc08]
    hub_environments[1].balloon_pointers = [0x7c5dc, 0x7c5e0]
    hub_environments[2].balloon_pointers = [0x7c5d4, 0x7c5d8]
    hub_environments[3].balloon_pointers = [0x7c3c8, 0x7c3cc]
    hub_environments[4].balloon_pointers = [0x7c5fc, 0x7c600]
    hub_environments[5].balloon_pointers = [0x7bb74, 0x7bb78]

    hub_environments[0].text_offset = 0x1006c
    hub_environments[1].text_offset = 0x1005c
    hub_environments[2].text_offset = 0x1004c
    hub_environments[3].text_offset = 0x1003c
    hub_environments[4].text_offset = 0x1002c
    hub_environments[5].text_offset = 0x1001c

    hub_environments[0].portal_dest_level_ids.append(0xc12b4)  # Stone Hill
    hub_environments[0].portal_dest_level_ids.append(0xc12a8)  # Dark Hollow
    hub_environments[0].portal_dest_level_ids.append(0xc12c0)  # Town Square
    hub_environments[0].portal_dest_level_ids.append(0xc129c)  # Toasty
    hub_environments[0].portal_dest_level_ids.append(0xc12cc)  # Sunny Flight

    hub_environments[1].portal_dest_level_ids.append(0xbfc48)  # Dry Canyon
    hub_environments[1].portal_dest_level_ids.append(0xbfc54)  # Cliff Town
    hub_environments[1].portal_dest_level_ids.append(0xbfc60)  # Ice Cavern
    hub_environments[1].portal_dest_level_ids.append(0xbfc6c)  # Doctor Shemp
    hub_environments[1].portal_dest_level_ids.append(0xbfc78)  # Night Flight

    hub_environments[2].portal_dest_level_ids.append(0xc627c)  # Alpine Ridge
    hub_environments[2].portal_dest_level_ids.append(0xc6294)  # High Caves
    hub_environments[2].portal_dest_level_ids.append(0xc6288)  # Wizard Peak
    hub_environments[2].portal_dest_level_ids.append(0xc6264)  # Blowhard
    hub_environments[2].portal_dest_level_ids.append(0xc6270)  # Crystal Flight

    hub_environments[3].portal_dest_level_ids.append(0xb558c)  # Terrace Village
    hub_environments[3].portal_dest_level_ids.append(0xb5574)  # Misty Bog
    hub_environments[3].portal_dest_level_ids.append(0xb5580)  # Tree Tops
    hub_environments[3].portal_dest_level_ids.append(0xb5568)  # Metalhead
    hub_environments[3].portal_dest_level_ids.append(0xb5598)  # Wild Flight

    hub_environments[4].portal_dest_level_ids.append(0xc5ecc)  # Dark Passage
    hub_environments[4].portal_dest_level_ids.append(0xc5ee4)  # Lofty Castle
    hub_environments[4].portal_dest_level_ids.append(0xc5efc)  # Haunted Towers
    hub_environments[4].portal_dest_level_ids.append(0xc5ed8)  # Jacques
    hub_environments[4].portal_dest_level_ids.append(0xc5ef0)  # Icy Flight

    hub_environments[5].portal_dest_level_ids.append(0xa69d8)  # Gnorc Cove
    hub_environments[5].portal_dest_level_ids.append(0xa69b4)  # Twilight Harbor
    hub_environments[5].portal_dest_level_ids.append(0xa69c0)  # Gnasty Gnorc
    hub_environments[5].portal_dest_level_ids.append(0xa69cc)  # Gnasty's Loot

    hub_environments[0].child_environments[0].text_offset = 0x101fc  # stone hill
    hub_environments[0].child_environments[1].text_offset = 0x101f0  # dark hollow
    hub_environments[0].child_environments[2].text_offset = 0x101e4  # town square
    hub_environments[0].child_environments[3].text_offset = 0x75570  # toasty
    hub_environments[0].child_environments[4].text_offset = 0x101d4  # sunny flight

    hub_environments[1].child_environments[0].text_offset = 0x101c8  # dry canyon
    hub_environments[1].child_environments[1].text_offset = 0x101bc  # cliff town
    hub_environments[1].child_environments[2].text_offset = 0x101b0  # ice cavern
    hub_environments[1].child_environments[3].text_offset = 0x101a0  # doctor shemp
    hub_environments[1].child_environments[4].text_offset = 0x10190  # night flight

    hub_environments[2].child_environments[0].text_offset = 0x10180  # alpine ridge
    hub_environments[2].child_environments[1].text_offset = 0x10174  # high caves
    hub_environments[2].child_environments[2].text_offset = 0x10168  # wizard peak
    hub_environments[2].child_environments[3].text_offset = 0x1015c  # blowhard
    hub_environments[2].child_environments[4].text_offset = 0x1014c  # crystal flight

    hub_environments[3].child_environments[0].text_offset = 0x1013c  # terrace village
    hub_environments[3].child_environments[1].text_offset = 0x10130  # misty bog
    hub_environments[3].child_environments[2].text_offset = 0x10124  # tree tops
    hub_environments[3].child_environments[3].text_offset = 0x10118  # metalhead
    hub_environments[3].child_environments[4].text_offset = 0x1010c  # wild flight

    hub_environments[4].child_environments[0].text_offset = 0x100fc  # dark passage
    hub_environments[4].child_environments[1].text_offset = 0x100ec  # lofty castle
    hub_environments[4].child_environments[2].text_offset = 0x100dc  # haunted towers
    hub_environments[4].child_environments[3].text_offset = 0x75568  # jacques
    hub_environments[4].child_environments[4].text_offset = 0x100d0  # icy flight

    hub_environments[5].child_environments[0].text_offset = 0x100b4  # gnorc cove
    hub_environments[5].child_environments[1].text_offset = 0x100a4  # twilight harbor
    hub_environments[5].child_environments[2].text_offset = 0x10094  # gnasty gnorc
    hub_environments[5].child_environments[3].text_offset = 0x10084  # gnasty's loot

    hub:SpyroEnvironment = hub_environments[0]
    for hub in hub_environments:
        dest_offset: int = 0
        for dest_offset in hub.portal_dest_level_ids:
            hub.portal_surface_types.append(dest_offset - 4)

    hub_environments[0].statue_head_checks = [
        0x7f48c,
        0x7f4c8
    ]
    hub_environments[5].statue_head_checks = [
        0x817fc,
        0x81810,
        0x81848,
        0x81884,
        0x8189c,
        0x818b4
    ]

    hub_environments[0].total_gems = 100
    hub_environments[0].child_environments[0].total_gems = 200
    hub_environments[0].child_environments[1].total_gems = 100
    hub_environments[0].child_environments[2].total_gems = 200
    hub_environments[0].child_environments[3].total_gems = 100
    hub_environments[0].child_environments[4].total_gems = 300
    hub_environments[1].total_gems = 200
    hub_environments[1].child_environments[0].total_gems = 400
    hub_environments[1].child_environments[1].total_gems = 400
    hub_environments[1].child_environments[2].total_gems = 400
    hub_environments[1].child_environments[3].total_gems = 300
    hub_environments[1].child_environments[4].total_gems = 300
    hub_environments[2].total_gems = 300
    hub_environments[2].child_environments[0].total_gems = 500
    hub_environments[2].child_environments[1].total_gems = 500
    hub_environments[2].child_environments[2].total_gems = 500
    hub_environments[2].child_environments[3].total_gems = 400
    hub_environments[2].child_environments[4].total_gems = 300
    hub_environments[3].total_gems = 300
    hub_environments[3].child_environments[0].total_gems = 400
    hub_environments[3].child_environments[1].total_gems = 500
    hub_environments[3].child_environments[2].total_gems = 500
    hub_environments[3].child_environments[3].total_gems = 500
    hub_environments[3].child_environments[4].total_gems = 300
    hub_environments[4].total_gems = 300
    hub_environments[4].child_environments[0].total_gems = 500
    hub_environments[4].child_environments[1].total_gems = 400
    hub_environments[4].child_environments[2].total_gems = 500
    hub_environments[4].child_environments[3].total_gems = 500
    hub_environments[4].child_environments[4].total_gems = 300
    hub_environments[5].total_gems = 200
    hub_environments[5].child_environments[0].total_gems = 400
    hub_environments[5].child_environments[1].total_gems = 400
    hub_environments[5].child_environments[2].total_gems = 500
    hub_environments[5].child_environments[3].total_gems = 2000

    hub_environments[0].gem_counter = 0x77420
    hub_environments[0].child_environments[0].gem_counter = 0x77424
    hub_environments[0].child_environments[1].gem_counter = 0x77428
    hub_environments[0].child_environments[2].gem_counter = 0x7742c
    hub_environments[0].child_environments[3].gem_counter = 0x77430
    hub_environments[0].child_environments[4].gem_counter = 0x77434
    hub_environments[1].gem_counter = 0x77438
    hub_environments[1].child_environments[0].gem_counter = 0x7743c
    hub_environments[1].child_environments[1].gem_counter = 0x77440
    hub_environments[1].child_environments[2].gem_counter = 0x77444
    hub_environments[1].child_environments[3].gem_counter = 0x77448
    hub_environments[1].child_environments[4].gem_counter = 0x7744c
    hub_environments[2].gem_counter = 0x77450
    hub_environments[2].child_environments[0].gem_counter = 0x77454
    hub_environments[2].child_environments[1].gem_counter = 0x77458
    hub_environments[2].child_environments[2].gem_counter = 0x7745c
    hub_environments[2].child_environments[3].gem_counter = 0x77460
    hub_environments[2].child_environments[4].gem_counter = 0x77464
    hub_environments[3].gem_counter = 0x77468
    hub_environments[3].child_environments[0].gem_counter = 0x7746c
    hub_environments[3].child_environments[1].gem_counter = 0x77470
    hub_environments[3].child_environments[2].gem_counter = 0x77474
    hub_environments[3].child_environments[3].gem_counter = 0x77478
    hub_environments[3].child_environments[4].gem_counter = 0x7747c
    hub_environments[4].gem_counter = 0x77480
    hub_environments[4].child_environments[0].gem_counter = 0x77484
    hub_environments[4].child_environments[1].gem_counter = 0x77488
    hub_environments[4].child_environments[2].gem_counter = 0x7748c
    hub_environments[4].child_environments[3].gem_counter = 0x77490
    hub_environments[4].child_environments[4].gem_counter = 0x77494
    hub_environments[5].gem_counter = 0x77498
    hub_environments[5].child_environments[0].gem_counter = 0x7749c
    hub_environments[5].child_environments[1].gem_counter = 0x774a0
    hub_environments[5].child_environments[2].gem_counter = 0x774a4
    hub_environments[5].child_environments[3].gem_counter = 0x774a8

    hub_environments[0].child_environments[0].vortex_moby_pointer = 0x177330
    hub_environments[0].child_environments[1].vortex_moby_pointer = 0x1339ac
    hub_environments[0].child_environments[2].vortex_moby_pointer = 0x17d644
    hub_environments[0].child_environments[3].vortex_moby_pointer = 0x1738ac

    hub_environments[1].child_environments[0].vortex_moby_pointer = 0x169444
    hub_environments[1].child_environments[1].vortex_moby_pointer = 0x16f978
    hub_environments[1].child_environments[2].vortex_moby_pointer = 0x16b454
    hub_environments[1].child_environments[3].vortex_moby_pointer = 0x16ba44

    hub_environments[2].child_environments[0].vortex_moby_pointer = 0x17bbec
    hub_environments[2].child_environments[1].vortex_moby_pointer = 0x17e188
    hub_environments[2].child_environments[2].vortex_moby_pointer = 0x179ce4
    hub_environments[2].child_environments[3].vortex_moby_pointer = 0x1396e4

    hub_environments[3].child_environments[0].vortex_moby_pointer = 0x179020
    hub_environments[3].child_environments[1].vortex_moby_pointer = 0x17b68c
    hub_environments[3].child_environments[2].vortex_moby_pointer = 0x17ce24
    hub_environments[3].child_environments[3].vortex_moby_pointer = 0x173fc4

    hub_environments[4].child_environments[0].vortex_moby_pointer = 0x178950
    hub_environments[4].child_environments[1].vortex_moby_pointer = 0x15a3d8
    hub_environments[4].child_environments[2].vortex_moby_pointer = 0x176964
    hub_environments[4].child_environments[3].vortex_moby_pointer = 0x16deb0

    hub_environments[5].child_environments[0].vortex_moby_pointer = 0x174884
    hub_environments[5].child_environments[1].vortex_moby_pointer = 0x17c298
    # Gnasty Gnorc has no vortex, skip
    hub_environments[5].child_environments[3].vortex_moby_pointer = 0x14da14

    # Collectibles stuff
    # Artisans
    hub_environments[0].dragons["Nestor"] = (0x77913, 0x01)
    hub_environments[0].dragons["Argus"] = (0x77913, 0x08)
    hub_environments[0].dragons["Delbin"] = (0x77919, 0x80)
    hub_environments[0].dragons["Tomas"] = (0x77913, 0x20)

    # Stone Hill
    hub_environments[0].child_environments[0].dragons["Lindar"] = (0x77932, 0x40)
    hub_environments[0].child_environments[0].dragons["Gavin"] = (0x7793d, 0x04)
    hub_environments[0].child_environments[0].dragons["Astor"] = (0x7793a, 0x01)
    hub_environments[0].child_environments[0].dragons["Gildas"] = (0x77939, 0x20)

    hub_environments[0].child_environments[0].eggs["Egg 1 (Upper Area)"] = (0x7793c, 0x40)

    # Dark Hollow
    hub_environments[0].child_environments[1].dragons["Alban"] = (0x77950, 0x02)
    hub_environments[0].child_environments[1].dragons["Oswin"] = (0x77953, 0x80)
    hub_environments[0].child_environments[1].dragons["Darius"] = (0x77955, 0x80)

    # Town Square
    hub_environments[0].child_environments[2].dragons["Nils"] = (0x77969, 0x10)
    hub_environments[0].child_environments[2].dragons["Thor"] = (0x77974, 0x20)
    hub_environments[0].child_environments[2].dragons["Alvar"] = (0x7796e, 0x02)
    hub_environments[0].child_environments[2].dragons["Devlin"] = (0x77969, 0x20)

    hub_environments[0].child_environments[2].eggs["Egg 1 (Upper Area)"] = (0x77973, 0x01)

    # Toasty
    hub_environments[0].child_environments[3].dragons["Nevin"] = (0x7798b, 0x01)

    # Peace Keepers
    hub_environments[1].dragons["Titan"] = (0x779cf, 0x02)
    hub_environments[1].dragons["Magnus"] = (0x779cf, 0x20)
    hub_environments[1].dragons["Gunnar"] = (0x779cf, 0x08)

    hub_environments[1].eggs["Egg 1 (Pool)"] = (0x779cd, 0x10)

    # Dry Canyon
    hub_environments[1].child_environments[0].dragons["Conan"] = (0x779fc, 0x20)
    hub_environments[1].child_environments[0].dragons["Boris"] = (0x779f2, 0x01)
    hub_environments[1].child_environments[0].dragons["Maximos"] = (0x779f2, 0x20)
    hub_environments[1].child_environments[0].dragons["Ivor"] = (0x779f2, 0x04)

    hub_environments[1].child_environments[0].eggs["Egg 1 (Starting Area)"] = (0x779f2, 0x80)

    # Cliff Town
    hub_environments[1].child_environments[1].dragons["Halvor"] = (0x77a1b, 0x80)
    hub_environments[1].child_environments[1].dragons["Enzo"] = (0x77a0f, 0x08)
    hub_environments[1].child_environments[1].dragons["Marco"] = (0x77a0f, 0x02)

    hub_environments[1].child_environments[1].eggs["Egg 1 (Square Building Past Bridge)"] = (0x77a1a, 0x04)

    # Ice Cavern
    hub_environments[1].child_environments[2].dragons["Ulric"] = (0x77a37, 0x08)
    hub_environments[1].child_environments[2].dragons["Todor"] = (0x77a41, 0x04)
    hub_environments[1].child_environments[2].dragons["Andor"] = (0x77a2b, 0x40)
    hub_environments[1].child_environments[2].dragons["Asher"] = (0x77a42, 0x08)
    hub_environments[1].child_environments[2].dragons["Ragnar"] = (0x77a30, 0x40)

    # Doctor Shemp
    hub_environments[1].child_environments[3].dragons["Trondo"] = (0x77a50, 0x08)

    # Magic Crafters
    hub_environments[2].dragons["Cosmos"] = (0x77a88, 0x40)
    hub_environments[2].dragons["Zantor"] = (0x77a8a, 0x40)
    hub_environments[2].dragons["Boldar"] = (0x77a8b, 0x01)

    hub_environments[2].eggs["Egg 1 (Entry)"] = (0x77a88, 0x01)
    hub_environments[2].eggs["Egg 2 (Courtyard)"] = (0x77a89, 0x40)

    # Alpine Ridge
    hub_environments[2].child_environments[0].dragons["Zane"] = (0x77aa9, 0x02)
    hub_environments[2].child_environments[0].dragons["Eldrid"] = (0x77aaa, 0x20)
    hub_environments[2].child_environments[0].dragons["Zander"] = (0x77abd, 0x10)
    hub_environments[2].child_environments[0].dragons["Kelvin"] = (0x77aac, 0x01)

    hub_environments[2].child_environments[0].eggs["Egg 1 (Distant Cave)"] = (0x77aad, 0x08)

    # High Caves
    hub_environments[2].child_environments[1].dragons["Cyrus"] = (0x77acf, 0x08)
    hub_environments[2].child_environments[1].dragons["Cedric"] = (0x77ad9, 0x80)
    hub_environments[2].child_environments[1].dragons["Ajax"] = (0x77ad1, 0x04)

    hub_environments[2].child_environments[1].eggs["Egg 1 (Distant Pool)"] = (0x77ad8, 0x40)
    hub_environments[2].child_environments[1].eggs["Egg 2 (Cave)"] = (0x77aca, 0x02)

    # Wizard Peak
    hub_environments[2].child_environments[2].dragons["Jarvis"] = (0x77aef, 0x80)
    hub_environments[2].child_environments[2].dragons["Hexus"] = (0x77aef, 0x40)
    hub_environments[2].child_environments[2].dragons["Lucas"] = (0x77ae8, 0x01)

    hub_environments[2].child_environments[2].eggs["Egg 1 (Quad-wizard Ramp)"] = (0x77af9, 0x08)
    hub_environments[2].child_environments[2].eggs["Egg 2 (End Area Pool)"] = (0x77aeb, 0x04)

    # Blowhard
    hub_environments[2].child_environments[3].dragons["Altair"] = (0x77b0b, 0x04)

    # Beast Makers
    hub_environments[3].dragons["Bruno"] = (0x77b48, 0x40)
    hub_environments[3].dragons["Cleetus"] = (0x77b49, 0x20)

    # Terrace Village
    hub_environments[3].child_environments[0].dragons["Claude"] = (0x77b6d, 0x20)
    hub_environments[3].child_environments[0].dragons["Cyprin"] = (0x77b6d, 0x80)

    # Misty Bog
    hub_environments[3].child_environments[1].dragons["Rosco"] = (0x77b93, 0x04)
    hub_environments[3].child_environments[1].dragons["Damon"] = (0x77b93, 0x10)
    hub_environments[3].child_environments[1].dragons["Zeke"] = (0x77b97, 0x08)
    hub_environments[3].child_environments[1].dragons["Bubba"] = (0x77b93, 0x40)

    # Tree Tops
    hub_environments[3].child_environments[2].dragons["Lyle"] = (0x77bb6, 0x80)
    hub_environments[3].child_environments[2].dragons["Jed"] = (0x77bb7, 0x02)
    hub_environments[3].child_environments[2].dragons["Isaak"] = (0x77bb6, 0x20)

    # Metalhead
    hub_environments[3].child_environments[3].dragons["Sadiki"] = (0x77bcc, 0x08)

    # Dream Weavers
    hub_environments[4].dragons["Mazi"] = (0x77c08, 0x80)
    hub_environments[4].dragons["Lateef"] = (0x77c19, 0x02)
    hub_environments[4].dragons["Zikomo"] = (0x77c08, 0x20)

    # Dark Passage
    hub_environments[4].child_environments[0].dragons["Kasiya"] = (0x77c28, 0x04)
    hub_environments[4].child_environments[0].dragons["Azizi"] = (0x77c28, 0x20)
    hub_environments[4].child_environments[0].dragons["Bakari"] = (0x77c28, 0x40)
    hub_environments[4].child_environments[0].dragons["Apara"] = (0x77c30, 0x20)
    hub_environments[4].child_environments[0].dragons["Obasi"] = (0x77c36, 0x01)

    # Lofty Castle
    hub_environments[4].child_environments[1].dragons["Mudada"] = (0x77c4f, 0x01)
    hub_environments[4].child_environments[1].dragons["Baruti"] = (0x77c49, 0x04)
    hub_environments[4].child_environments[1].dragons["Useni"] = (0x77c49, 0x01)

    # Haunted Towers
    hub_environments[4].child_environments[2].dragons["Kosoko"] = (0x77c6f, 0x20)
    hub_environments[4].child_environments[2].dragons["Lutalo"] = (0x77c70, 0x02)
    hub_environments[4].child_environments[2].dragons["Copano"] = (0x77c6f, 0x80)

    # Jacques
    hub_environments[4].child_environments[3].dragons["Unika"] = (0x77c8b, 0x80)
    hub_environments[4].child_environments[3].dragons["Revilo"] = (0x77c8d, 0x80)

    # Gnasty's World
    hub_environments[5].dragons["Delbin/Magnus"] = (0x77cc8, 0x01)

    # Gnorc Cove
    hub_environments[5].child_environments[0].dragons["Lateef"] = (0x77cf0, 0x20)
    hub_environments[5].child_environments[0].dragons["Tomas"] = (0x77ce8, 0x40)

    # Twilight Harbor
    hub_environments[5].child_environments[1].dragons["Cosmos"] = (0x77d09, 0x04)
    hub_environments[5].child_environments[1].dragons["Cleetus"] = (0x77d16, 0x10)

    cur_level_id: int = 0x7596c
    dest_level_id: int = 0x758b4
    cur_game_state: int = 0x757d8
    total_gem_count: int = 0x75860
    balloonist_menu_choice: int = 0x777f0
    unlocked_worlds: int = 0x758d0
    show_on_inventory_array: int = 0x78e78

    last_touched_whirlwind: int = 0x78c7c
    """Holds a pointer to the moby object for the last touched whirlwind."""

    starting_level_id: int = 0x2d4f0
    """Which level you start in after the intro cutscene."""

    gnasty_anim_flag: int = 0x160f08
    GNASTY_DEFEATED: int = 0x08

    nestor_unskippable: int = 0x1747f4
    tuco_egg_minimum: int = 0x8492c
    spyro_cur_animation: int = 0x78ad0
    spyro_color_filter: int = 0x78a80

    class SpyroStates(IntEnum):
        """Animation states for Spyro"""
        STANDING = 0x00
        FLOP = 0x06
        WHIRLWIND = 0x11
        ROLL = 0x13
        DEATH_SPIN = 0x1e

    class GameStates(IntEnum):
        """States the Spyro game engine can be in"""
        GAMEPLAY = 0x00
        LOADING = 0x01
        PAUSED = 0x02
        INVENTORY = 0x03
        DEATH = 0x04
        GAME_OVER = 0x05
        FLIGHT_MENU = 0x07
        DRAGON_CUTSCENE = 0x08
        FLY_IN = 0x09
        EXITING_LEVEL = 0x0a
        FAIRY_TEXTBOX = 0x0b
        BALLOONIST = 0x0c
        TITLE_SCREEN = 0x0d
        CUTSCENE = 0x0e
        CREDITS = 0x0f


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
