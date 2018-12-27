"""
Subcontroller module for Alien Invaders
"""
from game2d import *
from consts import *
from models import *
import random

class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
        _directionA: the direction (left or right) that the aliens are traveling
                     True if right, False if left [boolean]
        _verts: how many vertical positions the aliens have shifted downwards
                     True if 1, False if 0 [boolean]
        _alienFire: how many steps the alien is allowed to fire in [random int between 1 and BOLT_RATE]
        SCORE EXTENSION BELOW
        _score: Score of the current player. 10 points for a kill in the first row,
                20 for the next 2 rows, and then 30 for the next 2 [int >= 0]
        pewSound: Sound when either ship or alien bolt is fired [wav file]
        blastSound: Sound when ship is destroyed [wav file]
        blast2Sound: Sound when ship is destroyed [wav file]
        sound: if sound is wanted or not [boolean]
    """

    def setSound(self, a):
        self.sound = a

    def getSound(self):
        return self.sound

    def getShip(self):
        """
        Returns _ship of class Ship, stored in the _wave attribute of class Invaders

        Parameter self: a wave object
        Precondition: self is an object of class Wave
        """
        return self._ship

    def setShip(self, ship1):
        """
        Sets ship attribute in class Wave to parameter ship1

        Parameter ship1 is the new ship to set the _ship attribute to
        Precondition: ship1 is a Ship object
        """
        self._ship = ship1

    def getAliens(self):
        """
        Returns _aliens of class Aliens, a 2d list stored in the _wave attribute of class Invaders

        Parameter self: a wave object
        Precondition: self is an object of class Wave
        """
        return self._aliens

    def getdLine(self):
        """
        Returns _dline of class GPath, stored in the _wave attribute of class Invaders

        Parameter self: a wave object
        Precondition: self is an object of class Wave
        """
        return self._dline

    def getBolts(self):
        """
        Returns _bolts of class Bolt, stored in the _wave attribute of class Invaders

        Parameter self: a wave object
        Precondition: self is an object of class Wave
        """
        return self._bolts

    def getLives(self):
        """
        Returns _lives, stored in the _wave attribute of class Invaders

        Parameter self: a wave object
        Precondition: self is an object of class Wave
        """
        return self._lives

    def getScore(self):
        """
        Returns _score of class Ship, stored in the _wave attribute of class Invaders

        Parameter self: a wave object
        Precondition: self is an object of class Wave
        """
        return self._score
    def __init__(self):
        """
        Initializes attributes in class Wave when called from class Invaders
        SCORE EXTENSION
        """
        self._aliens = self.create2dAlien()
        self._ship = self.createShip()
        self._dline = GPath(points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth = 2,linecolor =[0.5,0.5,0,0.5])
        self._bolts = []
        self._time = 0
        self._directionA = True
        self._verts = False
        self._alienFire = random.randint(1, BOLT_RATE)
        self._lives = SHIP_LIVES
        self._score = 0
        self.pewSound = Sound('pew2.wav')
        self.blastSound = Sound('blast1.wav')
        self.blast2Sound = Sound('blast3.wav')
        self.sound = True

    def createShip(self):
        """
        Creates a ship centered horizontally and just below the defense line
        Returns: Ship object centered at position
        (GAME_WIDTH/2, SHIP_BOTTOM + SHIP_HEIGHT/2)
        """
        xShip = GAME_WIDTH/2
        yShip = SHIP_BOTTOM + SHIP_HEIGHT/2
        return Ship(xShip, yShip, 'ship.png')

    def create2dAlien(self):
        """
        Creates and returns a 2d list of aliens, with different aliens every two
        rows
        Returns: A 2d list of Alien objects
        """
        r = []
        xpos = ALIEN_H_SEP + ALIEN_WIDTH/2
        ypos = GAME_HEIGHT - ALIEN_CEILING - ALIEN_HEIGHT/2
        pos = len(ALIEN_IMAGES)-1
        image = ALIEN_IMAGES[pos]

        for a in range(0, ALIEN_ROWS):
            ypos = GAME_HEIGHT - ALIEN_CEILING - ALIEN_HEIGHT/2 - (1+a) * (ALIEN_HEIGHT + ALIEN_V_SEP)

            if ((ALIEN_ROWS - a)%2 == 0):
                pos = pos - 1

                if (pos == -1):
                    pos = len(ALIEN_IMAGES) - 1
                image = ALIEN_IMAGES[pos]

            for b in range(0, ALIENS_IN_ROW):
                r.append(Alien(xpos, ypos, image))
                xpos = xpos + ALIEN_WIDTH + ALIEN_H_SEP

            xpos = ALIEN_H_SEP + ALIEN_WIDTH/2

        a = []
        b = 0
        for x in range(0, len(r)):
            a.append(r[b:b+ALIENS_IN_ROW])
            b = b + ALIENS_IN_ROW
        return a
    def update(self, input, dt):
        """
        In charge of updating the positions, movements, and collisions of _ship,
        _aliens, and _bolts.

        Parameter input: The user input, used to control the ship and change state
        Precondition: input is an instance of GInput; it is inherited from GameApp

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if (self.getShip() != None):
            self.moveShip(input)
        self.moveAliens(dt)
        if (self.getShip() != None):
            self.createShipBolt(input)
        self.moveBolt()
        self.shipCollision()
        self.alienCollision()

    def isBelowLine(self):
        """
        Method to determine if any alien is below or touching the defense line
        Returns: True if any alien has reached defense line, False otherwise
        SOUND EXTENSION
        """
        for x in self.getAliens():
            for y in x:
                if (y != None):
                    if (y.y - ALIEN_HEIGHT/2 <= DEFENSE_LINE):
                        return True
                        if (self.sound):
                            self.blast2Sound.play()
        return False

    def noAliensAlive(self):
        """
        Method to determine if any aliens are still alive; if all of them have been
        destroyed
        Returns: True if there are no aliens alive, False if there is at least one
        alien alive
        """
        b = True
        for x in self.getAliens():
            for y in x:
                if (y != None):
                    b = False
        return b

    def shipCollision(self):
        """
        Method to determine if ship has been struck by an alien bolt. If ship has
        been hit, _ship is set to None, the corresponding bolt is deleted from
        _bolts, and the number of lives remaining is decremented by one
        SOUND EXTENSION
        """
        for x in self.getBolts():
            if (self._ship != None and self._ship.collides(x)):
                self._ship = None
                self.getBolts().remove(x)
                self._lives = self._lives - 1
                if (self.sound):
                    self.blast2Sound.play()

    def alienCollision(self):
        """
        Method to determine if any alien in _aliens has been struck by a ship bolt
        If alien is struck by ship bolt, alien is set to None and corresponding bolt
        is removed from _bolts. Score is increased by corresponding row number
        SOUND EXTENSION
        SCORE EXTENSION
        """
        a = None
        for x in self.getBolts():
            if (x.getVelocity() > 0):
                a = x
        for x in range(0, ALIEN_ROWS):
            for y in range(0, ALIENS_IN_ROW):
                if (a != None and self.getAliens()[x][y] != None
                and self.getAliens()[x][y].collides(a)):
                    self.getAliens()[x][y] = None
                    self.getBolts().remove(a)
                    if (self.sound):
                        self.blastSound.play()
                    if (x == 4):
                        self._score = self._score + 10
                    elif (x == 2 or x== 3):
                        self._score = self._score + 20
                    else:
                        self._score = self._score + 30

    def moveBolt(self):
        """
        Method to move all bolts currently on the game screen. If bolt travels
        off the screen, it is removed from _bolts
        """
        for a in self.getBolts():
            a.y = a.y + a.getVelocity()
            if (a.y > GAME_HEIGHT or a.y < 0):
                self.getBolts().remove(a)

    def createShipBolt(self, input):
        """
        Method to create a bolt traveling from the ship. There can only be one
        ship bolt on the game screen at one time, and a ship bolt is fired by
        pressing the 'spacebar' key
        SOUND EXTENSION
        """
        y = self.getShip().y + SHIP_HEIGHT/2
        canFire = True
        for x in self.getBolts():
            if (x.y < GAME_HEIGHT and x.isPlayerBolt()):
                canFire = False
        if (input.is_key_down('spacebar') and canFire):
            self.getBolts().append(Bolt(self.getShip().x, y, BOLT_SPEED))
            if (self.sound):
                self.pewSound.play()

    def moveAliens(self, dt):
        """
        Method moves aliens in a snaking fashion subject to parameter dt and
        calls createAlienBolt(), to create an alien bolt.

        Parameter dt: dt is the time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time = self._time + dt
        if (self._time > ALIEN_SPEED):
            self._time = 0
            if ((self.rightmostAlien() + ALIEN_H_SEP > GAME_WIDTH
            or self.leftmostAlien() < ALIEN_H_SEP) and self._verts):
                for x in self.getAliens():
                    for z in x:
                        if (z != None):
                            z.y = z.y - ALIEN_V_WALK
                self._verts = False
                if (self._directionA == True):
                    self._directionA = False
                else:
                    self._directionA = True
            elif (self._directionA == True):
                for x in self.getAliens():
                    for y in x:
                        if (y != None):
                            y.x = y.x + ALIEN_H_WALK
                self._verts = True
            elif (self._directionA == False):
                for x in self.getAliens():
                    for y in x:
                        if (y != None):
                            y.x = y.x - ALIEN_H_WALK
                self._verts = True
            self.createAlienBolt()

    def createAlienBolt(self):
        """
        Method checks if it is time to fire a bolt from an alien, using the
        attribute _alienFire
        """
        if (self._alienFire == 0):
            self.getBolts().append(self.pickAlien())
            self._alienFire = random.randint(1, BOLT_RATE)
        else:
            self._alienFire = self._alienFire - 1

    def pickAlien(self):
        """
        Method picks an alien to shoot a bolt out of. Checks where there are
        possible aliens to shoot out of, and then randomly selects an alien
        Returns a Bolt object traveling downwards towards the ship
        """
        b = False
        a = []
        for x in range(0, len(self.getAliens()[0])):
            b = False
            for y in range(0, ALIEN_ROWS):
                if (self.getAliens()[y][x] != None):
                    b = True
            if (b):
                a.append(x)

        z = random.randint(0, len(a) - 1)
        m = GAME_HEIGHT
        n = 0
        for y in range(0, ALIEN_ROWS):
            if (self.getAliens()[y][a[z]] != None):
                m = min(m, self.getAliens()[y][a[z]].y)
                n = self.getAliens()[y][a[z]].x
        return Bolt(n, m, -1 * BOLT_SPEED)

    def rightmostAlien(self):
        """
        Method finds the rightmost alien in the 2d list _aliens
        Returns x coordinate of the rightmost alien [int or float >= 0]
        """
        x = 0
        for a in self.getAliens():
            for b in a:
                if (b != None):
                    x = max(x, b.x)
        return x + ALIEN_WIDTH/2

    def leftmostAlien(self):
        """
        Method finds the leftmost alien in the 2d list _aliens
        Returns x coordinate of the leftmost alien [int or float >= 0]
        """
        x = GAME_WIDTH
        for a in self.getAliens():
            for b in a:
                if (b != None):
                    x = min(x, b.x)
        return x - ALIEN_WIDTH/2

    def moveShip(self, input):
        """
        Method moves _ship to the right or left given a player
        input of 'left' or 'right'
        """
        da = 0
        if (input.is_key_down('left')):
            da = da - SHIP_MOVEMENT
        if (input.is_key_down('right')):
            da = da + SHIP_MOVEMENT
        self._ship.x = self._ship.x + da
        if (self._ship.x > GAME_WIDTH - SHIP_WIDTH/2):
            self._ship.x = GAME_WIDTH - SHIP_WIDTH/2
        if (self._ship.x < SHIP_WIDTH/2):
            self._ship.x = SHIP_WIDTH/2
    def draw(self, view):
        """
        Method draws object in class Wave. If the object is None, the method
        doesn't do anything
        """
        if (self.getShip() != None):
            self.getShip().draw(view)
        for a in self.getAliens():
            for x in a:
                if (x != None):
                    x.draw(view)
        self.getdLine().draw(view)
        for a in self.getBolts():
            a.draw(view)
