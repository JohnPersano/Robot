

class Obstacle:
    """
    Class that holds data about obstacles.
    """

    class Type:
        """
        Enumeration for obstacle types
        """
        ROCK = 'rock'
        HOLE = 'hole'
        SPINNER = 'spinner'

    class Actions:
        DIRECT_POSITION = 'direct_position'
        POSITION_MODIFIER = 'position_modifier'
        DIRECTION_MODIFIER = 'direction_modifier'
        NO_MOVEMENT = 'no_movement'

    def __init__(self, location: tuple, ob_type: Type, actions: dict):
        self.location = location
        self.ob_type = ob_type
        self.actions = actions

    def _asdict(self):
        """
        Used for simplejson
        """
        return self.__dict__

    def __str__(self):
        return "Obstacle\n \tLocation: {}\n \tType: {}".format(self.location, self.ob_type)
