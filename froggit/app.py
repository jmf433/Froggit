"""
Primary module for Froggit

This module contains the main controller class for the Froggit application. There
is no need for any additional classes in this module.  If you need more classes, 99%
of the time they belong in either the lanes module or the models module. If you are
unsure about where a new class should go, post a question on Piazza.

John Fernandez jmf433
12/21/2020
"""
from consts import *
from game2d import *
from level import *
import introcs

from kivy.logger import Logger


# PRIMARY RULE: Froggit can only access attributes in level.py via getters/setters
# Froggit is NOT allowed to access anything in lanes.py or models.py.


class Froggit(GameApp):
    """
    The primary controller class for the Froggit application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Level object

        Method draw displays the Level object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Level.
    Level should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is managing the game state: when is the
    game started, paused, completed, etc. It keeps track of that in a hidden
    attribute

    Attribute view: The game view, used in drawing (see examples from class)
    Invariant: view is an instance of GView and is inherited from GameApp

    Attribute input: The user input, used to control the frog and change state
    Invariant: input is an instance of GInput and is inherited from GameApp
    """
    # Attribute _state: The current state of the game (taken from consts.py)
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED,
    #            STATE_ACTIVE, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _level: The subcontroller for a level, managing the frog and obstacles
    # Invariant: _level is a Level object or None if no level is currently active
    #
    # Attribute _title: The title of the game
    # Invariant: _title is a GLabel, or None if there is no title to display
    #
    # Attribute _text: A message to display to the player
    # Invariant: _text is a GLabel, or None if there is no message to display
    #
    # Attribute _lastS: Whether 's' key was pressed in the last frame or not
    # Invariant: _lastS is a bool
    #
    # Attribute _currentS: If 's' key is currently being pressed
    # Invariant: _currentS is a bool

    # Attribute _lastC: Whether 'c' key was pressed in the last frame or not
    # Invariant: _lastC is a bool
    #
    # Attribute _currentC: If 'c' key is currently being pressed
    # Invariant: _currentC is a bool

    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        creates both the title (in attribute _title) and a message (in attribute
        _text) saying that the user should press a key to play a game.
        """
        self._state = STATE_INACTIVE
        self._level = None

        if self._state == STATE_INACTIVE:
            self._title = GLabel(text='FROGGIT', font_name='Spongeboy.ttf')
            self._title.linecolor = 'dark green'
            self._title.font_size = ALLOY_LARGE
            self._title.x = self.width/2
            self._title.y = self.height/2

            self._text = GLabel(text="PRESS 'S' TO START",font_name='Spongeboy.ttf')
            self._text.font_size = ALLOY_MEDIUM
            self._text.x = self.width/2
            self._text.top = self._title.bottom

    def update(self,dt):
        """
        Updates the game objects each frame.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Level. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Level object _level to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_LOADING, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays the title and a simple message on the screen. The application
        remains in this state so long as the player never presses a key.

        STATE_LOADING: This is the state that creates a new level and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame (the amount of time to load
        the data from the file) before switching to STATE_ACTIVE. One of the
        key things about this state is that it resizes the window to match the
        level file.

        STATE_ACTIVE: This is a session of normal gameplay. The player can
        move the frog towards the exit, and the game will move all obstacles
        (cars and logs) about the screen. All of this should be handled inside
        of class Level (NOT in this class).  Hence the Level class should have
        an update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the frog after it was either killed
        or reached safety. The application switches to this state if the state
        was STATE_PAUSED in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over (all lives are lost or all frogs are safe),
        and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._stateInactive()
        elif self._state == STATE_LOADING:
            self._stateLoading()
        elif self._state == STATE_ACTIVE:
            self._stateActive(dt)
        elif self._state == STATE_PAUSED:
            self._statePaused()
        elif self._state == STATE_CONTINUE:
            self._stateContinue()
        elif self._state == STATE_COMPLETE:
            self._stateComplete()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. To draw a
        GObject g, simply use the method g.draw(self.view). It is that easy!

        Many of the GObjects (such as the cars, logs, and exits) are attributes
        in either Level or Lane. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        those two classes.  We suggest the latter.  See the example subcontroller.py
        from the lesson videos.
        """
        if self._state == STATE_INACTIVE:
            self._title.draw(self.view)
            self._text.draw(self.view)

    def _stateInactive(self):
        """
        Helper method for STATE_INACTIVE
        """
        self._lastS = False
        self._currentS = self.input.is_key_down('s')

        if self._currentS == True and self._lastS == False:
            self._state = STATE_LOADING
            self._title = None

    def _stateLoading(self):
        """
        Helper method for STATE_LOADING
        """
        level = self.load_json(DEFAULT_LEVEL)
        hitboxes = self.load_json(OBJECT_DATA)
        self.width = level['size'][0] * GRID_SIZE
        self.height = (level['size'][1] + 1) * GRID_SIZE
        self._level = Level(level,hitboxes)
        self._level.draw(self.view)
        self._state = STATE_ACTIVE

    def _stateActive(self,dt):
        """
        Helper method for STATE_ACTIVE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        level = self.load_json(DEFAULT_LEVEL)
        hitboxes = self.load_json(OBJECT_DATA)
        self._level.draw(self.view)
        self._text = None
        self._level.update(level,'none',dt,hitboxes)
        if self.input.is_key_down('up'):
            self._level.update(level,'up',dt,hitboxes)
        elif self.input.is_key_down('down'):
            self._level.update(level,'down',dt,hitboxes)
        elif self.input.is_key_down('right'):
            self._level.update(level,'right',dt,hitboxes)
        elif self.input.is_key_down('left'):
            self._level.update(level,'left',dt,hitboxes)
        self._level.draw(self.view)

        if self._level.getPauseGame():
            if self._level.getLCounter() == []:
                self._state = STATE_COMPLETE
            else:
                self._state = STATE_PAUSED

        elif self._level.getReachedExit():
            if self._level.getGameWin():
                self._state = STATE_COMPLETE
            else:
                self._state = STATE_PAUSED

    def _statePaused(self):
        """
        Helper method for STATE_PAUSED
        """
        self._lastC = False
        self._currentC = self.input.is_key_down('c')

        level = self.load_json(DEFAULT_LEVEL)
        self._level.draw(self.view)
        self._text = GLabel(text="PRESS 'C' TO CONTINUE",font_name='Spongeboy.ttf')
        self._text.font_size = ALLOY_SMALL
        self._text.x = self.width/2
        self._text.y = ((level['size'][1]/2)+(1/2))*GRID_SIZE
        self._text.fillcolor = 'white'
        self._text.draw(self.view)

        if self._currentC == True and self._lastC == False:
            self._text = None
            self._state = STATE_CONTINUE

    def _stateContinue(self):
        """
        Helper method for STATE_CONTINUE
        """
        level = self.load_json(DEFAULT_LEVEL)
        self._level.setFrogCollision(False)
        self._level.setReachedExit(False)
        self._level.setFrogX(level['start'][0] * GRID_SIZE + (GRID_SIZE / 2))
        self._level.setFrogY(level['start'][1] * GRID_SIZE + (GRID_SIZE / 2))
        self._level.setFrogAngle(FROG_NORTH)
        self._level.continueGame(level)
        self._level.draw(self.view)
        self._state = STATE_ACTIVE
        self._level.setAnimator(None)

    def _stateComplete(self):
        """
        Helper method for STATE_COMPLETE
        """
        if self._level.getGameWin():
            level = self.load_json(DEFAULT_LEVEL)
            self._level.draw(self.view)
            self._text = GLabel(text="YOU WIN!",font_name='Spongeboy.ttf')
            self._text.font_size = ALLOY_SMALL
            self._text.x = self.width/2
            self._text.y = ((level['size'][1]/2)+(1/2))*GRID_SIZE
            self._text.fillcolor = 'white'
            self._text.draw(self.view)
            self._stateComplete2()
        else:
            level = self.load_json(DEFAULT_LEVEL)
            self._level.draw(self.view)
            self._text = GLabel(text="GAME OVER",font_name='Spongeboy.ttf')
            self._text.font_size = ALLOY_SMALL
            self._text.x = self.width/2
            self._text.y = ((level['size'][1]/2)+(1/2))*GRID_SIZE
            self._text.fillcolor = 'white'
            self._text.draw(self.view)
            self._stateComplete2()

    def _stateComplete2(self):
        """
        Helper method for _stateComplete
        """
        self._lastR = False
        self._currentR = self.input.is_key_down('r')
        level = self.load_json(DEFAULT_LEVEL)

        self._text2= GLabel(text="RESTART? PRESS 'R'",
        font_name='Spongeboy.ttf')
        self._text2.font_size = ALLOY_SMALL
        self._text2.x = self.width/2
        self._text2.y = ((level['size'][1]/4)+(1/4))*GRID_SIZE
        self._text2.fillcolor = 'white'
        self._text2.draw(self.view)

        if self._currentR == True and self._lastR == False:
            self._text = None
            self._text2 = None
            self.width = GAME_WIDTH
            self.height = GAME_HEIGHT
            self.start()
