"""
Models module for Alien Invaders
"""
from consts import *
from game2d import *


class Ship(GImage):
    """
    A class to represent the game ship.
    """
    def __init__(self, x1, y1, source1):
        """
        Initializes GImage object representing a Ship with x position x1, y position y1,
        width of SHIP_WIDTH, height SHIP_HEIGHT, and a source of source1

        Parameter x1: x position to assign to GImage object
        Precondition: x1 is an int or float >= 0

        Parameter y1: y position to assign to GImage object
        Precondition: y1 is an int or float >= 0

        Parameter source1: source to assign to GImage object
        Precondition: source1 is a string corresponding to a png file in file directory
        """

        GImage.__init__(self, x = x1, y = y1, width = SHIP_WIDTH, height = SHIP_HEIGHT, source = source1)

    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by alien and collides with the ship

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if (bolt != None and bolt.getVelocity() > 0):
            return False
        a = self.contains((bolt.x + BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2))
        aa = self.contains((bolt.x + BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2))
        aaa = self.contains((bolt.x - BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2))
        aaaa = self.contains((bolt.x - BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2))
        return a or aa or aaa or aaaa


class Alien(GImage):
    """
    A class to represent a single alien.
    """

    def __init__(self, x1, y1, source1):
        """
        Initializes GImage object representing an Alien with x position x1, y position y1,
        width of ALIEN_WIDTH, height ALIEN_HEIGHT, and a source of source1

        Parameter x1: x position to assign to GImage object
        Precondition: x1 is an int or float >= 0

        Parameter y1: y position to assign to GImage object
        Precondition: y1 is an int or float >= 0

        Parameter source1: source to assign to GImage object
        Precondition: source1 is a string corresponding to a png file in file directory
        """
        GImage.__init__(self, x = x1, y = y1, width = ALIEN_WIDTH, height = ALIEN_HEIGHT, source = source1)

    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if (bolt != None and bolt.getVelocity() < 0):
            return False
        a = self.contains((bolt.x + BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2))
        aa = self.contains((bolt.x + BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2))
        aaa = self.contains((bolt.x - BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2))
        aaaa = self.contains((bolt.x - BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2))
        return a or aa or aaa or aaaa


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    """
    def getVelocity(self):
        """
        Returns velocity of Bolt object
        """
        return self._velocity
    def __init__(self, x1, y1, vel):
        """
        Initializes GRectangle object representing a Bolt with x position x1, y position y1,
        width of BOLT_WIDTH, height BOLT_HEIGHT, and a fillcolor of red
        Overrides __init__ method in GRectangle since Bolt also needs attribute _velocity

        Parameter x1: x position to assign to GRectangle object
        Precondition: x1 is an int or float >= 0

        Parameter y1: y position to assign to GRectangle object
        Precondition: y1 is an int or float >= 0

        Parameter vel: velocity to assign to GRectangle object
        Precondition: vel is an int or float >= 0
        """
        GRectangle.__init__(self, x = x1, y = y1, width = BOLT_WIDTH,
        height = BOLT_HEIGHT, fillcolor = 'red')
        self._velocity = vel


    def isPlayerBolt(self):
        """
        Method determines if a Bolt object was fired by the ship or an alien
        Returns True if fired by ship, Returns False if fired by alien
        """
        if (self._velocity > 0):
            return True
        return False
