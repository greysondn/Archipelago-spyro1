# pure python version of Spyro stuff goes here
import appetite.ap as ap


class Config(ap.Config):
    pass

class Connection(
    ap.Connection[
        "Region"
    ]
):
    pass

class Hub(
    ap.Container[
        "Hub", # but not really
        "Level",
        "Region",
        "Item",
        "Location",
        Config
    ]
):
    pass

class Item(ap.Item):
    pass

class Level(
    ap.Container[
        "Hub",
        "Level", # but not really
        "Region",
        Item,
        "Location",
        Config
    ]
):
    pass

class Location(ap.Location):
    pass

class Player(
    ap.Player[
        Item
    ]
):
    pass

class Region(
    ap.Region[
        Connection
    ]
):
    pass

class World(
    ap.GameWorld[
        Hub,
        Player
    ]
):
    pass