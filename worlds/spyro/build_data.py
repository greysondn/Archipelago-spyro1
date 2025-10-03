# Long story short, I asked Grok to analyze the object tree and then
# build conformant objects to it.
#
# The intent is to take these objects and build a working object tree,
# then dump that object tree out for later consumption.

class BHMemoryEntry:
    def __init__(self, address, length):
        self.address = address
        self.length = length

class Portal:
    def __init__(self):
        self.destination_address:int = 0x0

class AP:
    def __init__(self):
        self.groups = []

    def add_group(self, group):
        self.groups.append(group)

class SpyroHub:
    def __init__(self):
        self.name:str = "ERR"
        self.id:int = -1
        self.balloon_addresses:tuple[int, int] = (0, 0)
        self.text_offset = 0
        self.total_gems = -1
        self.gem_counter:BHMemoryEntry = BHMemoryEntry(0, 0)
        self.dragons = []
        self.eggs = []
        self.levels = []
        self.statue_head_checks = []

    def add_dragon(self, name, address, value):
        self.dragons.append({'name': name, 'address': address, 'value': value})

    def add_egg(self, name, address, value):
        self.eggs.append({'name': name, 'address': address, 'value': value})

    def add_level(self, level):
        self.levels.append(level)

class SpyroLevel:
    def __init__(self):
        self.name:str = "ERR"
        self.id:int = 0x00
        self.vortex_moby_pointer:int = 0x00
        self.text_offset:int = 0x00
        self.total_gems:int = -1
        self.gem_counter:BHMemoryEntry = BHMemoryEntry(0, 0)
        self.dragons = []
        self.eggs = []
        self.portal = Portal()
        self.ap = AP()
        self.statue_head_checks = None  # Some levels might use this, but not in code

    def add_dragon(self, name, address, value):
        self.dragons.append({'name': name, 'address': address, 'value': value})

    def add_egg(self, name, address, value):
        self.eggs.append({'name': name, 'address': address, 'value': value})

class SpyroGameWorld:
    def __init__(self):
        self.hubs = []

    def add_hub(self, hub):
        self.hubs.append(hub)

NO_POINTER = -1


world:SpyroGameWorld = SpyroGameWorld()

# hubs
artisans: SpyroHub = SpyroHub()
artisans.name = "Artisans"
artisans.id = 10
artisans.balloon_addresses = (0x7bc04, 0x7bc08)
artisans.text_offset = 0x1006c
artisans.total_gems = 100
artisans.gem_counter = BHMemoryEntry(0x77420, 2)
artisans.add_dragon("Nestor", 0x77913, 0x01)
artisans.add_dragon("Argus", 0x77913, 0x08)
artisans.add_dragon("Delbin", 0x77919, 0x80)
artisans.add_dragon("Tomas", 0x77913, 0x20)
artisans.statue_head_checks = [
    0x7f48c,
    0x7f4c8,
]

world.add_hub(artisans)

peace_keepers: SpyroHub = SpyroHub()
peace_keepers.name = "Peace Keepers"
peace_keepers.id = 20
peace_keepers.balloon_addresses = (0x7c5dc, 0x7c5e0)
peace_keepers.text_offset = 0x1005c
peace_keepers.total_gems = 200
peace_keepers.gem_counter = BHMemoryEntry(0x77438, 2)
peace_keepers.add_dragon("Titan", 0x779cf, 0x02)
peace_keepers.add_dragon("Magnus", 0x779cf, 0x20)
peace_keepers.add_dragon("Gunnar", 0x779cf, 0x08)
peace_keepers.add_egg("Egg 1 (Pool)", 0x779cd, 0x10)
world.add_hub(peace_keepers)

magic_crafters: SpyroHub = SpyroHub()
magic_crafters.name = "Magic Crafters"
magic_crafters.id = 30
magic_crafters.balloon_addresses = (0x7c5d4, 0x7c5d8)
magic_crafters.text_offset = 0x1004c
magic_crafters.total_gems = 300
magic_crafters.gem_counter = BHMemoryEntry(0x77450, 2)
magic_crafters.add_dragon("Cosmos", 0x77a88, 0x40)
magic_crafters.add_dragon("Zantor", 0x77a8a, 0x40)
magic_crafters.add_dragon("Boldar", 0x77a8b, 0x01)
magic_crafters.add_egg("Egg 1 (Entry)", 0x77a88, 0x01)
magic_crafters.add_egg("Egg 2 (Courtyard)", 0x77a89, 0x40)
world.add_hub(magic_crafters)

beast_makers: SpyroHub = SpyroHub()
beast_makers.name = "Beast Makers"
beast_makers.id = 40
beast_makers.balloon_addresses = (0x7c3c8, 0x7c3cc)
beast_makers.text_offset = 0x1003c
beast_makers.total_gems = 300
beast_makers.gem_counter = BHMemoryEntry(0x77468, 2)
beast_makers.add_dragon("Bruno", 0x77b48, 0x40)
beast_makers.add_dragon("Cleetus", 0x77b49, 0x20)
world.add_hub(beast_makers)

dream_weavers: SpyroHub = SpyroHub()
dream_weavers.name = "Dream Weavers"
dream_weavers.id = 50
dream_weavers.balloon_addresses = (0x7c5fc, 0x7c600)
dream_weavers.text_offset = 0x1002c
dream_weavers.total_gems = 300
dream_weavers.gem_counter = BHMemoryEntry(0x77480, 2)
dream_weavers.add_dragon("Mazi", 0x77c08, 0x80)
dream_weavers.add_dragon("Lateef", 0x77c19, 0x02)
dream_weavers.add_dragon("Zikomo", 0x77c08, 0x20)
world.add_hub(dream_weavers)

gnastys_world: SpyroHub = SpyroHub()
gnastys_world.name = "Gnasty's World"
gnastys_world.id = 60
gnastys_world.balloon_addresses = (0x7bb74, 0x7bb78)
gnastys_world.text_offset = 0x1001c
gnastys_world.total_gems = 200
gnastys_world.gem_counter = BHMemoryEntry(0x77498, 2)
gnastys_world.add_dragon("Delbin/Magnus", 0x77cc8, 0x01)
gnastys_world.statue_head_checks = [
    0x817fc,
    0x81810,
    0x81848,
    0x81884,
    0x8189c,
    0x818b4,
]
world.add_hub(gnastys_world)

# artisans
stone_hill:SpyroLevel = SpyroLevel()
stone_hill.name = "Stone Hill"
stone_hill.id = 11
stone_hill.vortex_moby_pointer = 0x177330
stone_hill.text_offset = 0x101fc
stone_hill.total_gems = 200
stone_hill.gem_counter = BHMemoryEntry(0x77424, 2)
stone_hill.add_dragon("Lindar", 0x77932, 0x40)
stone_hill.add_dragon("Gavin", 0x7793d, 0x04)
stone_hill.add_dragon("Astor", 0x7793a, 0x01)
stone_hill.add_dragon("Gildas", 0x77939, 0x20)
stone_hill.add_egg("Egg 1 (Upper Area)", 0x7793c, 0x40)
stone_hill.portal.destination_address = 0xc12b4
artisans.add_level(stone_hill)

dark_hollow:SpyroLevel = SpyroLevel()
dark_hollow.name = "Dark Hollow"
dark_hollow.id = 12
dark_hollow.vortex_moby_pointer = 0x1339ac
dark_hollow.text_offset = 0x101f0
dark_hollow.total_gems = 100
dark_hollow.gem_counter = BHMemoryEntry(0x77428, 2)
dark_hollow.add_dragon("Alban", 0x77950, 0x02)
dark_hollow.add_dragon("Oswin", 0x77953, 0x80)
dark_hollow.add_dragon("Darius", 0x77955, 0x80)
dark_hollow.portal.destination_address = 0xc12a8
artisans.add_level(dark_hollow)

town_square:SpyroLevel = SpyroLevel()
town_square.name = "Town Square"
town_square.id = 13
town_square.vortex_moby_pointer = 0x17d644
town_square.text_offset = 0x101e4
town_square.total_gems = 200
town_square.gem_counter = BHMemoryEntry(0x7742c, 2)
town_square.add_dragon("Nils", 0x77969, 0x10)
town_square.add_dragon("Thor", 0x77974, 0x20)
town_square.add_dragon("Alvar", 0x7796e, 0x02)
town_square.add_dragon("Devlin", 0x77969, 0x20)
town_square.add_egg("Egg 1 (Upper Area)", 0x77973, 0x01)
town_square.portal.destination_address = 0xc12c0
artisans.add_level(town_square)

toasty:SpyroLevel = SpyroLevel()
toasty.name = "Toasty"
toasty.id = 14
toasty.vortex_moby_pointer = 0x1738ac
toasty.text_offset = 0x75570
toasty.total_gems = 100
toasty.gem_counter = BHMemoryEntry(0x77430, 2)
toasty.add_dragon("Nevin", 0x7798b, 0x01)
toasty.portal.destination_address = 0xc129c
toasty.ap.add_group("Boss Levels")
artisans.add_level(toasty)

sunny_flight:SpyroLevel = SpyroLevel()
sunny_flight.name = "Sunny Flight"
sunny_flight.id = 15
sunny_flight.vortex_moby_pointer = NO_POINTER
sunny_flight.text_offset = 0x101d4
sunny_flight.total_gems = 300
sunny_flight.gem_counter = BHMemoryEntry(0x77434, 2)
sunny_flight.portal.destination_address = 0xc12cc
sunny_flight.ap.add_group("Flight Levels")
artisans.add_level(sunny_flight)

# peace keepers
dry_canyon:SpyroLevel = SpyroLevel()
dry_canyon.name = "Dry Canyon"
dry_canyon.id = 21
dry_canyon.vortex_moby_pointer = 0x169444
dry_canyon.text_offset = 0x101c8
dry_canyon.total_gems = 400
dry_canyon.gem_counter = BHMemoryEntry(0x7743c, 2)
dry_canyon.add_dragon("Conan", 0x779fc, 0x20)
dry_canyon.add_dragon("Boris", 0x779f2, 0x01)
dry_canyon.add_dragon("Maximos", 0x779f2, 0x20)
dry_canyon.add_dragon("Ivor", 0x779f2, 0x04)
dry_canyon.add_egg("Egg 1 (Starting Area)", 0x779f2, 0x80)
dry_canyon.portal.destination_address = 0xbfc48
peace_keepers.add_level(dry_canyon)

cliff_town:SpyroLevel = SpyroLevel()
cliff_town.name = "Cliff Town"
cliff_town.id = 22
cliff_town.vortex_moby_pointer = 0x16f978
cliff_town.text_offset = 0x101bc
cliff_town.total_gems = 400
cliff_town.gem_counter = BHMemoryEntry(0x77440, 2)
cliff_town.add_dragon("Halvor", 0x77a1b, 0x80)
cliff_town.add_dragon("Enzo", 0x77a0f, 0x08)
cliff_town.add_dragon("Marco", 0x77a0f, 0x02)
cliff_town.add_egg("Egg 1 (Square Building Past Bridge)", 0x77a1a, 0x04)
cliff_town.portal.destination_address = 0xbfc54
peace_keepers.add_level(cliff_town)

ice_cavern:SpyroLevel = SpyroLevel()
ice_cavern.name = "Ice Cavern"
ice_cavern.id = 23
ice_cavern.vortex_moby_pointer = 0x16b454
ice_cavern.text_offset = 0x101b0
ice_cavern.total_gems = 400
ice_cavern.gem_counter = BHMemoryEntry(0x77444, 2)
ice_cavern.add_dragon("Ulric", 0x77a37, 0x08)
ice_cavern.add_dragon("Todor", 0x77a41, 0x04)
ice_cavern.add_dragon("Andor", 0x77a2b, 0x40)
ice_cavern.add_dragon("Asher", 0x77a42, 0x08)
ice_cavern.add_dragon("Ragnar", 0x77a30, 0x40)
ice_cavern.portal.destination_address = 0xbfc60
peace_keepers.add_level(ice_cavern)

doctor_shemp:SpyroLevel = SpyroLevel()
doctor_shemp.name = "Doctor Shemp"
doctor_shemp.id = 24
doctor_shemp.vortex_moby_pointer = 0x16ba44
doctor_shemp.text_offset = 0x101a0
doctor_shemp.total_gems = 300
doctor_shemp.gem_counter = BHMemoryEntry(0x77448, 2)
doctor_shemp.add_dragon("Trondo", 0x77a50, 0x08)
doctor_shemp.portal.destination_address = 0xbfc6c
doctor_shemp.ap.add_group("Boss Levels")
peace_keepers.add_level(doctor_shemp)

night_flight:SpyroLevel = SpyroLevel()
night_flight.name = "Night Flight"
night_flight.id = 25
night_flight.vortex_moby_pointer = NO_POINTER
night_flight.text_offset = 0x10190
night_flight.total_gems = 300
night_flight.gem_counter = BHMemoryEntry(0x7744c, 2)
night_flight.portal.destination_address = 0xbfc78
night_flight.ap.add_group("Flight Levels")
peace_keepers.add_level(night_flight)

# magic crafters
alpine_ridge:SpyroLevel = SpyroLevel()
alpine_ridge.name = "Alpine Ridge"
alpine_ridge.id = 31
alpine_ridge.vortex_moby_pointer = 0x17bbec
alpine_ridge.text_offset = 0x10180
alpine_ridge.total_gems = 500
alpine_ridge.gem_counter = BHMemoryEntry(0x77454, 2)
alpine_ridge.add_dragon("Zane", 0x77aa9, 0x02)
alpine_ridge.add_dragon("Eldrid", 0x77aaa, 0x20)
alpine_ridge.add_dragon("Zander", 0x77abd, 0x10)
alpine_ridge.add_dragon("Kelvin", 0x77aac, 0x01)
alpine_ridge.add_egg("Egg 1 (Distant Cave)", 0x77aad, 0x08)
alpine_ridge.portal.destination_address = 0xc627c
magic_crafters.add_level(alpine_ridge)

high_caves:SpyroLevel = SpyroLevel()
high_caves.name = "High Caves"
high_caves.id = 32
high_caves.vortex_moby_pointer = 0x17e188
high_caves.text_offset = 0x10174
high_caves.total_gems = 500
high_caves.gem_counter = BHMemoryEntry(0x77458, 2)
high_caves.add_dragon("Cyrus", 0x77acf, 0x08)
high_caves.add_dragon("Cedric", 0x77ad9, 0x80)
high_caves.add_dragon("Ajax", 0x77ad1, 0x04)
high_caves.add_egg("Egg 1 (Distant Pool)", 0x77ad8, 0x40)
high_caves.add_egg("Egg 2 (Cave)", 0x77aca, 0x02)
high_caves.portal.destination_address = 0xc6294
magic_crafters.add_level(high_caves)

wizard_peak:SpyroLevel = SpyroLevel()
wizard_peak.name = "Wizard Peak"
wizard_peak.id = 33
wizard_peak.vortex_moby_pointer = 0x179ce4
wizard_peak.text_offset = 0x10168
wizard_peak.total_gems = 500
wizard_peak.gem_counter = BHMemoryEntry(0x7745c, 2)
wizard_peak.add_dragon("Jarvis", 0x77aef, 0x80)
wizard_peak.add_dragon("Hexus", 0x77aef, 0x40)
wizard_peak.add_dragon("Lucas", 0x77ae8, 0x01)
wizard_peak.add_egg("Egg 1 (Quad-wizard Ramp)", 0x77af9, 0x08)
wizard_peak.add_egg("Egg 2 (End Area Pool)", 0x77aeb, 0x04)
wizard_peak.portal.destination_address = 0xc6288
magic_crafters.add_level(wizard_peak)

blowhard:SpyroLevel = SpyroLevel()
blowhard.name = "Blowhard"
blowhard.id = 34
blowhard.vortex_moby_pointer = 0x1396e4
blowhard.text_offset = 0x1015c
blowhard.total_gems = 400
blowhard.gem_counter =BHMemoryEntry(0x77460, 2)
blowhard.add_dragon("Altair", 0x77b0b, 0x04)
blowhard.portal.destination_address = 0xc6264
blowhard.ap.add_group("Boss Levels")
magic_crafters.add_level(blowhard)

crystal_flight:SpyroLevel = SpyroLevel()
crystal_flight.name = "Crystal Flight"
crystal_flight.id = 35
crystal_flight.vortex_moby_pointer = NO_POINTER
crystal_flight.text_offset = 0x1014c
crystal_flight.total_gems = 300
crystal_flight.gem_counter = BHMemoryEntry(0x77464, 2)
crystal_flight.portal.destination_address = 0xc6270
crystal_flight.ap.add_group("Flight Levels")
magic_crafters.add_level(crystal_flight)

# beast makers
terrace_village: SpyroLevel = SpyroLevel()
terrace_village.name = "Terrace Village"
terrace_village.id = 41
terrace_village.vortex_moby_pointer = 0x179020
terrace_village.text_offset = 0x1013c
terrace_village.total_gems = 400
terrace_village.gem_counter = BHMemoryEntry(0x7746c, 2)
terrace_village.add_dragon("Claude", 0x77b6d, 0x20)
terrace_village.add_dragon("Cyprin", 0x77b6d, 0x80)
terrace_village.portal.destination_address = 0xb558c
beast_makers.add_level(terrace_village)

misty_bog: SpyroLevel = SpyroLevel()
misty_bog.name = "Misty Bog"
misty_bog.id = 42
misty_bog.vortex_moby_pointer = 0x17b68c
misty_bog.text_offset = 0x10130
misty_bog.total_gems = 500
misty_bog.gem_counter = BHMemoryEntry(0x77470, 2)
misty_bog.add_dragon("Rosco", 0x77b93, 0x04)
misty_bog.add_dragon("Damon", 0x77b93, 0x10)
misty_bog.add_dragon("Zeke", 0x77b97, 0x08)
misty_bog.add_dragon("Bubba", 0x77b93, 0x40)
misty_bog.portal.destination_address = 0xb5574
beast_makers.add_level(misty_bog)

tree_tops: SpyroLevel = SpyroLevel()
tree_tops.name = "Tree Tops"
tree_tops.id = 43
tree_tops.vortex_moby_pointer = 0x17ce24
tree_tops.text_offset = 0x10124
tree_tops.total_gems = 500
tree_tops.gem_counter = BHMemoryEntry(0x77474, 2)
tree_tops.add_dragon("Lyle", 0x77bb6, 0x80)
tree_tops.add_dragon("Jed", 0x77bb7, 0x02)
tree_tops.add_dragon("Isaak", 0x77bb6, 0x20)
tree_tops.portal.destination_address = 0xb5580
beast_makers.add_level(tree_tops)

metalhead: SpyroLevel = SpyroLevel()
metalhead.name = "Metalhead"
metalhead.id = 44
metalhead.vortex_moby_pointer = 0x173fc4
metalhead.text_offset = 0x10118
metalhead.total_gems = 500
metalhead.gem_counter = BHMemoryEntry(0x77478, 2)
metalhead.add_dragon("Sadiki", 0x77bcc, 0x08)
metalhead.portal.destination_address = 0xb5568
metalhead.ap.add_group("Boss Levels")
beast_makers.add_level(metalhead)

wild_flight: SpyroLevel = SpyroLevel()
wild_flight.name = "Wild Flight"
wild_flight.id = 45
wild_flight.vortex_moby_pointer = NO_POINTER
wild_flight.text_offset = 0x1010c
wild_flight.total_gems = 300
wild_flight.gem_counter = BHMemoryEntry(0x7747c, 2)
wild_flight.portal.destination_address = 0xb5598
wild_flight.ap.add_group("Flight Levels")
beast_makers.add_level(wild_flight)

# dream weavers
dark_passage: SpyroLevel = SpyroLevel()
dark_passage.name = "Dark Passage"
dark_passage.id = 51
dark_passage.vortex_moby_pointer = 0x178950
dark_passage.text_offset = 0x100fc
dark_passage.total_gems = 500
dark_passage.gem_counter = BHMemoryEntry(0x77484, 2)
dark_passage.add_dragon("Kasiya", 0x77c28, 0x04)
dark_passage.add_dragon("Azizi", 0x77c28, 0x20)
dark_passage.add_dragon("Bakari", 0x77c28, 0x40)
dark_passage.add_dragon("Apara", 0x77c30, 0x20)
dark_passage.add_dragon("Obasi", 0x77c36, 0x01)
dark_passage.portal.destination_address = 0xc5ecc
dream_weavers.add_level(dark_passage)

lofty_castle: SpyroLevel = SpyroLevel()
lofty_castle.name = "Lofty Castle"
lofty_castle.id = 52
lofty_castle.vortex_moby_pointer = 0x15a3d8
lofty_castle.text_offset = 0x100ec
lofty_castle.total_gems = 400
lofty_castle.gem_counter = BHMemoryEntry(0x77488, 2)
lofty_castle.add_dragon("Mudada", 0x77c4f, 0x01)
lofty_castle.add_dragon("Baruti", 0x77c49, 0x04)
lofty_castle.add_dragon("Useni", 0x77c49, 0x01)
lofty_castle.portal.destination_address = 0xc5ee4
dream_weavers.add_level(lofty_castle)

haunted_towers: SpyroLevel = SpyroLevel()
haunted_towers.name = "Haunted Towers"
haunted_towers.id = 53
haunted_towers.vortex_moby_pointer = 0x176964
haunted_towers.text_offset = 0x100dc
haunted_towers.total_gems = 500
haunted_towers.gem_counter = BHMemoryEntry(0x7748c, 2)
haunted_towers.add_dragon("Kosoko", 0x77c6f, 0x20)
haunted_towers.add_dragon("Lutalo", 0x77c70, 0x02)
haunted_towers.add_dragon("Copano", 0x77c6f, 0x80)
haunted_towers.portal.destination_address = 0xc5efc
dream_weavers.add_level(haunted_towers)

jacques: SpyroLevel = SpyroLevel()
jacques.name = "Jacques"
jacques.id = 54
jacques.vortex_moby_pointer = 0x16deb0
jacques.text_offset = 0x75568
jacques.total_gems = 500
jacques.gem_counter = BHMemoryEntry(0x77490, 2)
jacques.add_dragon("Unika", 0x77c8b, 0x80)
jacques.add_dragon("Revilo", 0x77c8d, 0x80)
jacques.portal.destination_address = 0xc5ed8
jacques.ap.add_group("Boss Levels")
dream_weavers.add_level(jacques)

icy_flight: SpyroLevel = SpyroLevel()
icy_flight.name = "Icy Flight"
icy_flight.id = 55
icy_flight.vortex_moby_pointer = NO_POINTER
icy_flight.text_offset = 0x100d0
icy_flight.total_gems = 300
icy_flight.gem_counter = BHMemoryEntry(0x77494, 2)
icy_flight.portal.destination_address = 0xc5ef0
icy_flight.ap.add_group("Flight Levels")
dream_weavers.add_level(icy_flight)

# gnasty's world
gnorc_cove: SpyroLevel = SpyroLevel()
gnorc_cove.name = "Gnorc Cove"
gnorc_cove.id = 61
gnorc_cove.vortex_moby_pointer = 0x174884
gnorc_cove.text_offset = 0x100b4
gnorc_cove.total_gems = 400
gnorc_cove.gem_counter = BHMemoryEntry(0x7749c, 2)
gnorc_cove.add_dragon("Lateef", 0x77cf0, 0x20)
gnorc_cove.add_dragon("Tomas", 0x77ce8, 0x40)
gnorc_cove.portal.destination_address = 0xa69d8
gnastys_world.add_level(gnorc_cove)

twilight_harbor: SpyroLevel = SpyroLevel()
twilight_harbor.name = "Twilight Harbor"
twilight_harbor.id = 62
twilight_harbor.vortex_moby_pointer = 0x17c298
twilight_harbor.text_offset = 0x100a4
twilight_harbor.total_gems = 400
twilight_harbor.gem_counter = BHMemoryEntry(0x774a0, 2)
twilight_harbor.add_dragon("Cosmos", 0x77d09, 0x04)
twilight_harbor.add_dragon("Cleetus", 0x77d16, 0x10)
twilight_harbor.portal.destination_address = 0xa69b4
gnastys_world.add_level(twilight_harbor)

gnasty_gnorc: SpyroLevel = SpyroLevel()
gnasty_gnorc.name = "Gnasty Gnorc"
gnasty_gnorc.id = 63
gnasty_gnorc.vortex_moby_pointer = NO_POINTER
gnasty_gnorc.text_offset = 0x10094
gnasty_gnorc.total_gems = 500
gnasty_gnorc.gem_counter = BHMemoryEntry(0x774a4, 2)
gnasty_gnorc.portal.destination_address = 0xa69c0
gnasty_gnorc.ap.add_group("Boss Levels")
gnastys_world.add_level(gnasty_gnorc)

gnastys_loot: SpyroLevel = SpyroLevel()
gnastys_loot.name = "Gnasty's Loot"
gnastys_loot.id = 64
gnastys_loot.vortex_moby_pointer = 0x14da14
gnastys_loot.text_offset = 0x10084
gnastys_loot.total_gems = 2000
gnastys_loot.gem_counter = BHMemoryEntry(0x774a8, 2)
gnastys_loot.portal.destination_address = 0xa69cc
gnastys_world.add_level(gnastys_loot)