"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

John Fernandez jmf433
12/21/2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """
    # Attribute _lanes: A list containing what to draw for each lane
    # Invariant: _lanes is a list of GTile objects

    # Attribute _frog: The frog object for Froggit
    # Invariant: _frog is a Frog object

    # Attribute _liveCounter: A list containing the frog heads that display lives
    # Invariant: _liveCounter is a list of GImages objects

    # Attribute _liveText: The text for the live counter
    # Invariant: _liveText is a GLabel object

    # Attribute _delay: The amount of time to delay before the frog can move again
    # Invariant: _delay is an int or a bool

    # Attribute _frogcollision: Bool that tells whether or not the frog was hit by car
    # Invariant: _frogcollision is a bool

    # Attribute _hedgeLanes: A list that tells us which lanes are of the class: 'Hedge'
    # Invariant: _hedgeLanes is a list of ints

    # Attribute _reachedExit: Bool that tells us if frog has reached an exit
    # Invariant: _reachedExit is a bool

    # Attribute _gameWin: Bool that tells us if player has won game
    # Invariant: _gameWin is a bool

    # Attribute _totalExits: Int that tells us the total amount of exits in the level
    # Invariant: _totalExits is an int

    # Attribute _totalSafeFrogs: Int that tells us how many safe frogs there are
    # Invariant: _totalSafeFrogs is an int

    # Attribute _animator: Bool or None that tells us if frog is currenly animating
    # Invariant: _animator is a bool or None

    # Attribute _blocked: Bool that tells us if the frog's path is currently blocked
    # Invariant: _blocked is a bool

    # Attribute _waterLanes: A list that tells us whihc lanes are of the class: "Water"
    # Invariant: _waterLanes is a list of ints

    # Attribute _safe: A bool that tells us whether the frog is safe on a log
    # Invariant: _safe is a bool

    # Attribute _opening: A bool that tells us whether there is an opening in a hedge
    # Invariant: _opening is a bool

    # Attribute _death: The death object for Frog object
    # Invariant: _death is a Death object

    # Attribute _deathAnimation: A bool that tells us if the death animation is running
    # Invariant: _deathAnimation is a bool

    # Attribute _pauseGame: A bool that tells us whether or not to pause the game
    # Invariant: _pauseGame is a bool

    def getFrogX(self):
        """
        Getter for the x position of the frog
        """
        return self._frog.getX()

    def getFrogY(self):
        """
        Getter for the y position of the frog
        """
        return self._frog.getY()

    def setFrogX(self,value):
        """
        Setter for the x position of the frog

        Parameter value: The value to set x to
        Precondition: value is an int or float
        """
        self._frog.setX(value)

    def setFrogY(self,value):
        """
        Setter for the y position of the frog

        Parameter value: The value to set y to
        Precondition: value is an int or float
        """
        self._frog.setY(value)

    def getFrogCollision(self):
        """
        Getter for for the bool that determines if the frog has collided
        with an object
        """
        return self._frogcollision

    def setFrogCollision(self,value):
        """
        Setter for for the bool that determines if the frog has collided
        with an object

        Parameter value: The bool value to change the attribute to
        Precondition: value is a bool
        """
        self._frogcollision = value

    def setFrogAngle(self,value):
        """
        Setter for the angle the frog is facing

        Parameter value: The angle value to change the frog to
        Precondition: Value is int between 0 and 360 (inclusive)
        """
        self._frog.angle = value

    def getLCounter(self):
        """
        Getter for self._liveCounter
        """
        return self._liveCounter

    def getReachedExit(self):
        """
        Getter for for the bool that determines if the frog has reached an exit
        with an object
        """
        return self._reachedExit

    def setReachedExit(self,value):
        """
        Setter for for the bool that determines if the frog has reached an exit

        Parameter value: The bool value to change the attribute to
        Precondition: value is a bool
        """
        self._reachedExit = value

    def getGameWin(self):
        """
        Getter for the bool that determines if game has been won
        """
        return self._gameWin

    def setAnimator(self,value):
        """
        Setter for the animator bool

        Parameter value: The bool to change the attribute to
        Precondition: value is a bool or None
        """
        self._animator = value

    def getPauseGame(self):
        """
        Getter for the bool that determines if the game should pause
        """
        return self._pauseGame

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self,level,hitboxes):
        """
        Initializes the level object for Froggit

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file

        Parameter hitboxes: The preloaded json file that contains the hitboxes
        for the objects in the game
        Precondition: hitboxes is a preloaded json file
        """
        # Creates the lanes for the level
        self._lanes = []
        self._totalExits = 0
        self._totalSafeFrogs = 0
        self._delay = 0
        self._opening = False
        self._frogcollision = False
        self._reachedExit = False
        self._gameWin = False
        self._animator = None
        self._animator2 = None
        self._blocked = False
        self._deathAnimation = True
        self._pauseGame = False
        self._trill = False
        for x in range(level['size'][1]):
            if level['lanes'][x]['type'] == 'grass':
                lane = Grass(level,x,hitboxes)
            elif level['lanes'][x]['type'] == 'road':
                lane = Road(level,x,hitboxes)
            elif level['lanes'][x]['type'] == 'water':
                lane = Water(level,x,hitboxes)
            else:
                lane = Hedge(level,x,hitboxes)
            self._lanes.append(lane)
        #Creates the frog and death sprite for the level
        self._frog = Frog(level['start'][0],level['start'][1],hitboxes)
        self._death = Death(level['start'][0],level['start'][1])
        #Creates the live counter
        self._createLcounter(level)

    def update(self,level,keyInput,dt,hitboxes):
        """
        Updates Frog object and the objects in each lane

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file

        Parameter keyInput: The current key being pressed
        Precondition: keyInput is a str

        Parameter dt: The time in seconds since last update
        Precondition: dt is an int or a float

        Parameter hitboxes: The preloaded json file that contains the hitboxes
        for the objects in the game
        Precondition: hitboxes is a preloaded json file
        """
        # Updating obstacles and frog collisions
        if keyInput == 'none':
            for x in range(len(self._lanes)):
                if (level['lanes'][x]['type'] != 'grass' and
                level['lanes'][x]['type'] != 'hedge'):
                    self._lanes[x].update(x,dt,level)
                if level['lanes'][x]['type'] == 'road':
                    for y in range(len(level['lanes'][x]['objects'])):
                        collide = self._lanes[x].getObjs()[y].collides(self._frog)
                        if collide:
                            self._animator = None
                            self._frogcollision = True
        # Frog riding on log
        if self._frogcollision != True:
            if self._animator == None and self._blocked == False:
                waterLanes = self._findWater(level)
                for x in range(len(waterLanes)):
                    self._logRide(waterLanes[x],dt,level)
        self._blocked = False
        # Frog hitboxes
        currentFrame = self._frog.frame
        self.hitbox = hitboxes['sprites']['frog']['hitboxes'][currentFrame]
        # Movement of the Frog
        self._trill = False
        self._frogMovement(level,keyInput,dt,hitboxes)
        self._death.setX(self._frog.getX())
        self._death.setY(self._frog.getY())
        if self._frogcollision == True and self._pauseGame == False:
            self._animateDeath(dt)

    def draw(self,view):
        """
        Draws the lanes and frog for Froggit

        Parameter view: The window to draw the lanes on
        Precondition: view is a valid window
        """
        for lane in range(len(self._lanes)):
            self._lanes[lane].draw(view)
        if self._frogcollision == False and self._reachedExit == False:
            self._frog.draw(view)
        if self._frogcollision == True and self._pauseGame == False:
            self._death.draw(view)
        for frog in range(len(self._liveCounter)):
            self._liveCounter[frog].draw(view)
        self._liveText.draw(view)

    def continueGame(self,level):
        """
        Helper method to reset frog and continute the game

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        self._frog.setX(level['start'][0] * GRID_SIZE + (GRID_SIZE / 2))
        self._frog.setY(level['start'][1] * GRID_SIZE + (GRID_SIZE / 2))
        self._frog.angle = FROG_NORTH
        self._frogcollision = False
        self._pauseGame = False
        self._frog.frame = 0

    def _animateDeath(self,dt):
        """
        Helper method for update that creates the death animation for Froggit

        Parameter dt: The time in seconds since last update
        Precondition: dt is an int or a float
        """
        if not self._animator2 is None:          # We have something to animate
            try:
                self._animator2.send(dt)
            except:
                self._animator2 = None
                self._pauseGame = True
                self._liveCounter = self._liveCounter[:-1]

        elif self._frogcollision == True and self._pauseGame == False:
            self._animator2 = self._death.deathAnimation(dt)
            next(self._animator2)

    def _frogMovement(self,level,keyInput,dt,hitboxes):
        """
        Helper method for update that controls the movement of the frog
        depending on user input

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file

        Parameter keyInput: The current key being pressed
        Precondition: keyInput is a str

        Parameter dt: The time in seconds since last update
        Precondition: dt is an int or a float

        Parameter hitboxes: The preloaded json file that contains the hitboxes
        for the objects in the game
        Precondition: hitboxes is a preloaded json file
        """
        if not self._animator is None:
            try:
                self._animator.send(dt)
                currentFrame = self._frog.frame
                self.hitbox = hitboxes['sprites']['frog']['hitboxes'][currentFrame]
            except StopIteration:
                self._animator = None
                self._delay = FROG_SPEED

        if keyInput != 'none':
            if self._delay <= 0:
                if self._animator == None:
                    self._createGenerator(level,keyInput)
            else:
                self._delay -= dt

    def _createGenerator(self,level,keyInput):
        """
        Helper method for _frogMovement that creates the generator for the
        coroutine

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file

        Parameter keyInput: The current key being pressed
        Precondition: keyInput is a str
        """
        if keyInput == 'up':
            if self._moveUp(level):
                self._animator = self._frog.slideAnimation(keyInput,self._trill)
                next(self._animator)
            else:
                self._blocked = True
        elif keyInput == 'down':
            if self._moveDown(level):
                self._animator = self._frog.slideAnimation(keyInput,False)
                next(self._animator)
        elif keyInput == 'right':
            if self._moveRight(level):
                self._animator = self._frog.slideAnimation(keyInput,False)
                next(self._animator)
        elif keyInput == 'left':
            if self._moveLeft(level):
                self._animator = self._frog.slideAnimation(keyInput,False)
                next(self._animator)

    def _createLcounter(self,level):
        """
        Helper method to create the live counter for Froggit

        Parameter level: The json file for the current level
        Precondition: level is a preloaded json file
        """
        #Creates the frog heads
        self._liveCounter = []
        for x in range(3):
            source = 'froghead.png'
            frogHead = GImage(width=GRID_SIZE,height=GRID_SIZE,source=source)
            frogHead.left = (level['size'][0]-3+x) * GRID_SIZE
            frogHead.top = (level['size'][1]+1) * GRID_SIZE
            self._liveCounter.append(frogHead)

        #Creates the text for live counter
        self._liveText = GLabel(text="LIVES:",font_name='Spongeboy.ttf')
        self._liveText.font_size = ALLOY_SMALL
        self._liveText.linecolor = "dark green"
        self._liveText.right = self._liveCounter[0].left
        self._liveText.bottom = level['size'][1] * GRID_SIZE - (GRID_SIZE // 5)

    def _findHedge(self,level):
        """
        Helper method to find the position(s) of Hedge objects in self._lanes

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        self._hedgeLanes = []
        for x in range(level['size'][1]):
            if level['lanes'][x]['type'] == 'hedge':
                self._hedgeLanes.append(x)
        return self._hedgeLanes

    def _findWater(self,level):
        """
        Helper method to find the position(s) of Water objects in self._lanes

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        self._waterLanes = []
        for x in range(level['size'][1]):
            if level['lanes'][x]['type'] == 'water':
                self._waterLanes.append(x)
        return self._waterLanes

    def _moveUp(self,level):
        """
        Helper method to move the frog forward

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        newVar = True
        self._opening = False
        self._frog.angle = FROG_NORTH
        self.setFrogY(self.getFrogY() + GRID_SIZE)
        for y in range(len(self._findHedge(level))):
            if Lane.getTile(self._lanes[self._hedgeLanes[y]]).collides(self._frog):
                newVar = False
                list = Hedge.getObjs(self._lanes[self._hedgeLanes[y]])
                frogList = Hedge.getSafeFrogs(self._lanes[self._hedgeLanes[y]])
                for x in range(len(list)):
                    if list[x].contains((self.getFrogX(),self.getFrogY())):
                        currentLane = self._lanes[self._hedgeLanes[y]]
                        objPos = x
                        if self._checkSafeFrogs(y) == True:
                            newVar = False
                        elif currentLane.opening(objPos,level):
                            self._opening = True
                            newVar = True
                        else:
                            currentLane.reachExit(objPos,level)
                            self._reachedExit = True
                            self._trill = True
                            newVar = True
                if self._exitsComplete(level):
                    self._gameWin = True
        if newVar == True:
            self._delay = FROG_SPEED
        self.setFrogY(self.getFrogY() - GRID_SIZE)
        return newVar

    def _moveDown(self,level):
        """
        Helper method to move the frog downward

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        newVar = True
        self._opening = False
        self._frog.angle = FROG_SOUTH
        self.setFrogY(self.getFrogY() - GRID_SIZE)
        for y in range(len(self._findHedge(level))):
            if Lane.getTile(self._lanes[self._hedgeLanes[y]]).collides(self._frog):
                list = Hedge.getObjs(self._lanes[self._hedgeLanes[y]])
                for x in range(len(list)):
                    if list[x].contains((self.getFrogX(),self.getFrogY())):
                        currentLane = self._lanes[self._hedgeLanes[y]]
                        objPos = x
                        if currentLane.opening(objPos,level):
                            self._opening = True
                        else:
                            newVar = False
        if self.getFrogY() - GRID_SIZE > 0:
            for x in range(len(self._findHedge(level))):
                if Lane.getTile(self._lanes[self._hedgeLanes[x]]).collides(self._frog):
                    newVar = False
        if self.getFrogY() <= 0:
            newVar = False
        if self._opening == True:
            newVar = True
        self.setFrogY(self.getFrogY() + GRID_SIZE)
        if newVar == True:
            self._delay = FROG_SPEED
        return newVar

    def _moveRight(self,level):
        """
        Helper method to move the frog rightward

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        newVar = True
        self._frog.angle = FROG_EAST
        if not (self.getFrogX() + GRID_SIZE < (level['size'][0]*GRID_SIZE)):
            newVar = False
        if self._opening == True:
            newVar = False
        if newVar == True:
            self._delay = FROG_SPEED
        return newVar

    def _moveLeft(self,level):
        """
        Helper method to move the frog leftward

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        newVar = True
        self._frog.angle = FROG_WEST
        if not (self.getFrogX() - GRID_SIZE > 0):
            newVar = False
        if self._opening == True:
            newVar = False
        if newVar == True:
            self._delay = FROG_SPEED
        return newVar

    def _checkSafeFrogs(self,y):
        """
        Helper method to check if the current exit is occupied by Safe Frog

        Parameter y: The position in hedgeLanes to check
        Precondition: y is in range of self._hedgeLanes
        """
        exp = False
        frogList = Hedge.getSafeFrogs(self._lanes[self._hedgeLanes[y]])
        for x in range(len(frogList)):
            if frogList[x].contains((self.getFrogX(),self.getFrogY())):
                exp = True
        return exp

    def _exitsComplete(self,level):
        """
        Helper method to determine the number of exits there are for the frog
        land safely on in order to win the level and if each space has been
        complete. Returns a bool

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        winner = False
        for y in range(len(self._findHedge(level))):
            frogList = Hedge.getSafeFrogs(self._lanes[self._hedgeLanes[y]])
            newAmt = Hedge.numberOfExits(self._lanes[self._hedgeLanes[y]])
            self._totalExits += newAmt
            self._totalSafeFrogs += len(frogList)
        if self._totalSafeFrogs == self._totalExits:
            winner = True
        self._totalExits = 0
        self._totalSafeFrogs = 0
        return winner

    def _logRide(self,pos,dt,level):
        """
        Helper method the mvoes the frog along with log object

        Parameter pos: The position of the lane in the json file
        Precondition: object is a GImage object

        Parameter dt: The time in seconds since last update
        Precondition: dt is an int or a float

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        self._safe = False
        speed = level['lanes'][pos]['speed']
        width = level['size'][0] * GRID_SIZE
        dist = speed*dt
        frog = (self._frog.getX(),self._frog.getY())
        if self._lanes[pos].getTile().contains(frog):
            for y in range(len(self._lanes[pos].getObjs())):
                collide = self._lanes[pos].getObjs()[y].contains(frog)
                if collide:
                    self._frog.setX(self._frog.getX()+dist)
                    self._safe = True
        if self._lanes[pos].getTile().contains(frog) and not self._safe:
            self._frogcollision = True
            self._animator = None
        elif self._frog.getX() <= 0:
            self._frogcollision = True
            self._animator = None
        elif self._frog.getX() >= width:
            self._frogcollision = True
            self._animator = None
