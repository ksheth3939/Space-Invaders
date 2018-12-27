"""
Primary module for Alien Invaderss
"""
from consts import *
from game2d import *
from wave import *

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    INSTANCE ATTRIBUTES:
        view:    the game view, used in drawing (see examples from class)
                 [instance of GView; it is inherited from GameApp]
        input:   the user input, used to control the ship and change state
                 [instance of GInput; it is inherited from GameApp]
        _state:  the current state of the game represented as a value from consts.py
                 [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:   the subcontroller for a single wave, which manages the ships and aliens
                 [Wave, or None if there is no wave currently active]
        _text:   the currently active message
                 [GLabel, or None if there is no message to display]
        lastkeys: number of keys pressed in the previous frame [int >= 0]
        soundOn: GLabel displaying sound text box if sound on
        soundOff: GLabel displaying sound text box if sound off
    """

    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self.lastkeys = 0
        self._soundOn = GLabel(text ="S to change sound\nSound is on",font_size=25,bold=True,x=GAME_WIDTH/2,y=.92*GAME_HEIGHT)
        self._soundOff = GLabel(text ="S to change sound\nSound is off",font_size=25,bold=True,x=GAME_WIDTH/2,y=.92*GAME_HEIGHT)
        if (self._state == STATE_INACTIVE):
            self._text = GLabel(text = "Press 'Q' to Play", font_size = 100, bold = True, x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        else:
            self._text = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        current = self.input.key_count
        if (current > 0 and self.lastkeys == 0):
            if (self.input.is_key_down('q') == True and self._state == STATE_INACTIVE):
                self._state = STATE_NEWWAVE
                self._text = None
        self.lastkeys = current
        if (self._state == STATE_NEWWAVE):
            self._wave = Wave()
            self._state = STATE_ACTIVE
        self.active(dt)
        if (self._state == STATE_PAUSED and self.input.is_key_down('f') == True):
            if (self._wave.getLives() > 0):
                self._state = STATE_ACTIVE
                self._wave.setShip(self._wave.createShip())
            else:
                self._text=GLabel(text="Sorry you're bad\nNo lives left\nPress P to Play Again\nYour score was "+str(self._wave.getScore()),font_size=70,bold=True,x=GAME_WIDTH/2,y=GAME_HEIGHT/2)
                self._state = STATE_COMPLETE

        if (self._state == STATE_COMPLETE and self.input.is_key_down('p')):
            self.start()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        if (self._state == STATE_INACTIVE):
            self._text.draw(self.view)

        if (self._state == STATE_NEWWAVE):
            self._wave.draw(self.view)

        if (self._state == STATE_ACTIVE):
            self._wave.draw(self.view)
            self._text.draw(self.view)
            if (self._wave.getSound()):
                self._soundOn.draw(self.view)
            else:
                self._soundOff.draw(self.view)

        if (self._state == STATE_PAUSED):
            self._wave.draw(self.view)
            self._text.draw(self.view)

        if (self._state == STATE_COMPLETE):
            self._text.draw(self.view)
    # HELPER METHODS FOR THE STATES GO HERE
    def active(self, dt):
        """
        Method updates game when state is STATE_ACTIVE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if (self._state == STATE_ACTIVE):
            self._wave.update(self.input, dt)
            current = self.input.key_count
            if (self.input.is_key_down('s') and current > 0):
                if (self._wave.getSound()):
                    self._wave.setSound(False)
                else:
                    self._wave.setSound(True)
            self.lastkeys = current
            if (self._wave.isBelowLine()):
                self._text=GLabel(text ="Sorry you're bad\nShip crossed line\nPress F to Play Again\nYour score was " + str(self._wave.getScore()),font_size=70,bold=True,x=GAME_WIDTH/2,y=GAME_HEIGHT/2)
                self._state = STATE_COMPLETE
            elif (self._wave.noAliensAlive()):
                self._text=GLabel(text="Good Win",font_size=100,bold=True,x=GAME_WIDTH/2,y=GAME_HEIGHT/2)
                self._state = STATE_COMPLETE
            elif (self._wave.getShip() == None):
                self._text=GLabel(text="Press 'F' to Respwan\nYou have "+str(self._wave.getLives())+' lives left'
                ,font_size=70,bold=True,x=GAME_WIDTH/2,y=GAME_HEIGHT/2)
                self._state = STATE_PAUSED
            else:
                self._text = GLabel(text="Lives: "+str(self._wave.getLives())+'     Score: '+str(self._wave.getScore()),
                font_size=25,bold=True,x=GAME_WIDTH/2,y=.85*GAME_HEIGHT)
