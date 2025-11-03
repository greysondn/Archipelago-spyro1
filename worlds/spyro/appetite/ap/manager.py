"""
Module for singleton managers for things that are purely python and related to
core Archipelago needs.
"""

class IndexManager(object):
    """Singleton.
        
    Manages AP indexes on a per-game basis, in order to keep them
    unique and consistent.
    
    Simply create the object and request the next index for your game using 
    get_next(). It can handle the rest via magic for you.
    """
    _instance:"IndexManager | None" = None
    """The only instance of this class"""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IndexManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # We would like to present to you some forbidden, black magic that will
        # make you scream "NO! THAT NOT ONLY DOESN'T GO THERE, BUT IT SHOULDN'T
        # EVER WORK! NO! NO! NO! NO!"
        if not hasattr(self, "_initialized"):
            # do init
            self._initialized:bool = True
            """Whether or not this has been initialized."""
            
            self._current:dict[str,int] = {}
    
    def get_next(self, game:str) -> int:
        """Get the next valid int out of this manager.
        
        The manager maintains per-game indexes based on their names. Two games
        will have two different indexes.
        
        Args:
            game: Which game this is for. 
        """
        ret:int = self._current.get(game, 1)
        
        self._current[game] = ret + 1
        
        return ret