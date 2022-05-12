"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

John Fernandez jmf433
12/21/2020
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GSprite):
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """
    # Attribute _x: The x coordinate of the frog
    # Invariant: _x is an int or float

    # Attribute _y: The y coordinate of the frog
    # Invariant: _y is an int or float

    # Attribute _wait: The time to wait on frame 4
    # Invariant: _wait is an int

    # Attribute _time: The amount of time that the frog has been animating
    # Invariant: _time is a float

    # Attribute _frac: A float that tells us the amount of distance frog has traveled
    # Invariant: _frac is a float

    # Attribute _fvert: A float that tells us the final y position of the frog
    # Invariant: _fvert is a float

    # Attribute _fhori: A float that tells us the final x position of the frog
    # Invariant: _fhori is a float

    # Attribute _animating: bool that tells us whether or not the frog is animating
    # Invariant: _animating is a bool

    # Attribute _jumpSound: sound that plays whenever the frog jumps normally
    # Invariant: _jumpSound is a Sound object

    # Attribute _trillSound: sound that plays whenever the frog reaches lilypad
    # Invariant: _trillSound is a Sound object

    def getX(self):
        """
        Getter for x
        """
        return self.x

    def setX(self,value):
        """
        Setter for x

        Parameter value: A value to change the x coordinate of frog to
        Precondition: value is a float or an int
        """
        self.x = value

    def getY(self):
        """
        Getter for y
        """
        return self.y

    def setY(self,value):
        """
        Setter for y

        Parameter value: A value to change the y coordinate of frog to
        Precondition: value is a float or an int
        """
        self.y = value

    def __init__(self,x,y,hitboxes):
        """
        Initializes the frog object for Froggit

        Parameter x: The starting x coordinate for the frog
        Precondition: x is an int or a float

        Parameter y: The starting y coordinate for the frog
        Precondition: y is an int or a float

        Parameter hitboxes: The preloaded json file that contains the hitboxes
        for the objects in the game
        Precondition: hitboxes is a preloaded json file
        """
        self._jumpSound = Sound(CROAK_SOUND)
        self._trillSound = Sound(TRILL_SOUND)
        x = (x * GRID_SIZE) + (GRID_SIZE // 2)
        y = (y * GRID_SIZE) + (GRID_SIZE // 2)
        source = FROG_SPRITE + '.png'
        super().__init__(x=x,y=y,source=source,format=(1,5))
        self.angle = FROG_NORTH
        self.frame = 0
        self.hitbox = hitboxes['sprites']['frog']['hitboxes'][0]

    def slideAnimation(self,keyInput,trill):
        """
        Animates the frog when moving

        Parameter keyInput: The current key being pressed
        Precondition: keyInput is a str

        Parameter trill: A bool telling us whether or not to play the trill sound
        Precondition: trill is a bool
        """
        if trill:
            self._trillSound.play()
        else:
            self._jumpSound.play()
        self._wait = 0
        self._time = 0
        self._frac = 0
        svert = self.y
        shori = self.x
        fvert = 0
        fhori = 0
        self._fvert = 0
        self._fhori = 0
        value = self._direction(keyInput,svert,shori)
        fvert = self._fvert
        fhori = self._fhori
        if value < 3:
            steps = (fvert - svert) / FROG_SPEED
        elif value > 2:
            steps = (fhori - shori) / FROG_SPEED
        self._animating = True
        while self._animating:
            dt = (yield)
            amount = steps * dt
            if value < 3:
                self.y += amount
            elif value > 2:
                self.x += amount
            self._animation1(value,svert,shori,fvert,fhori)
            self._animation2(value,svert,shori,fvert,fhori)
            self._snap(value,svert,shori,fvert,fhori,dt)

    def _direction(self,keyInput,svert,shori):
        """
        Helper method for slideAnimation that returns a value for direction
        of the Frog's movement

        Parameter svert: The beginning y position of the frog in the animation
        Precondition: svert is an int or float

        Parameter shori: The beginning x position of the frog in the animation
        Precondition: shori is an int or float

        Parameter keyInput: The current key being pressed
        Precondition: keyInput is a str
        """
        if keyInput == 'up':
            self.angle = FROG_NORTH
            value = 1
            self._fvert = svert + GRID_SIZE
        elif keyInput == 'down':
            self.angle = FROG_SOUTH
            value = 2
            self._fvert = svert - GRID_SIZE
        elif keyInput == 'right':
            self.angle = FROG_EAST
            value = 3
            self._fhori = shori + GRID_SIZE
        elif keyInput == 'left':
            self.angle = FROG_WEST
            value = 4
            self._fhori = shori - GRID_SIZE
        return value

    def _animation1(self,value,svert,shori,fvert,fhori):
        """
        Helper method for slideAnimation that moves the frog

        Parameter value: The value that is attributed to a certain direction
        Precondition: Value is an int between 1 and 4 (inclusive)

        Parameter svert: The beginning y position of the frog in the animation
        Precondition: svert is an int or float

        Parameter shori: The beginning x position of the frog in the animation
        Precondition: shori is an int or float

        Parameter fvert: The ending y position of the frog in the animation
        Precondition: fvert is an int or float

        Parameter fhori: The ending x position of the frog in the animation
        Precondition: fhori is an int or float
        """
        if value < 3:
            frac = 2 * abs((self.y-svert)) / GRID_SIZE
            if frac < 1:
                frame = frac * 4
                self.frame = round(frame)
            else:
                frac = frac - 1
                frame = 4 - (frac * 4)
                if frame > -(.5):
                    self.frame = round(frame)
                else:
                    self.frame = 0
                if self.frame == 0:
                    self.y = fvert

    def _animation2(self,value,svert,shori,fvert,fhori):
        """
        Helper method for slideAnimation that moves the frog

        Parameter value: The value that is attributed to a certain direction
        Precondition: Value is an int between 1 and 4 (inclusive)

        Parameter svert: The beginning y position of the frog in the animation
        Precondition: svert is an int or float

        Parameter shori: The beginning x position of the frog in the animation
        Precondition: shori is an int or float

        Parameter fvert: The ending y position of the frog in the animation
        Precondition: fvert is an int or float

        Parameter fhori: The ending x position of the frog in the animation
        Precondition: fhori is an int or float
        """
        if value > 2:
            frac = 2 * abs((self.x-shori)) / GRID_SIZE
            if frac < 1:
                frame = frac * 4
                self.frame = round(frame)
            else:
                self.frame = 4
                if self._wait == 1:
                    frac = frac - 1
                    frame = 4 - (frac * 4)
                    if frame > -(.5):
                        self.frame = round(frame)
                    else:
                        self.frame = 0
                    if self.frame == 0:
                        self.x = fhori
                self._wait = 1

    def _snap(self,value,svert,shori,fvert,fhori,dt):
        """
        Helper method for slideAnimation that snaps frog in place

        Parameter value: The value that is attributed to a certain direction
        Precondition: Value is an int between 1 and 4 (inclusive)

        Parameter svert: The beginning y position of the frog in the animation
        Precondition: svert is an int or float

        Parameter shori: The beginning x position of the frog in the animation
        Precondition: shori is an int or float

        Parameter fvert: The ending y position of the frog in the animation
        Precondition: fvert is an int or float

        Parameter fhori: The ending x position of the frog in the animation
        Precondition: fhori is an int or float

        Parameter dt: The time in seconds since last update
        Precondition: dt is a an int or float
        """
        if value < 3:
            if abs(self.y - svert) >= GRID_SIZE:
                self.y = fvert
                self._animating = False
                self.frame = 0
        if value > 2:
            if abs(self.x - shori) >= GRID_SIZE:
                self.x = fhori
                self._animating = False
                self.frame = 0
        self._time += dt
        if self._time >= FROG_SPEED:
            self.animating = False
            if value < 3:
                self.y = fvert
                self._animating = False
                self.frame = 0
            if value > 2:
                self.x = fhori
                self._animating = False
                self.frame = 0


class Death(GSprite):
    """
    A class representing the death animation

    This death animation is represented as a sprite and is called whenever
    the frog dies in Froggit and displays where the frog died
    """
    # Attribute _animating: bool that tells us whether the object is animating
    # Invariant: _animating is a bool

    # Attribute _time: a float that tells us the amount of time that has elapsed
    # Invariant: _time is a float

    # Attribute _deathSound: the sound the frog makes when it dies
    # Invariant: _deathSound is a Sound object

    def setX(self,value):
        """
        Setter for the x coordinate of the death animation

        Parameter value: A float to change the x coordinate to
        Precondition: value is a bool
        """
        self.x = value

    def setY(self,value):
        """
        Setter for the y coordinate of the death animation

        Parameter value: A float to change the y coordinate to
        Precondition: value is a bool
        """
        self.y = value

    def __init__(self,x,y):
        """
        Initializes the death object for Froggit

        Parameter x: The starting x coordinate for the object
        Precondition: x is an int or a float

        Parameter y: The starting y coordinate for the frog
        Precondition: y is an int or a float
        """
        self._deathSound = Sound(SPLAT_SOUND)
        x = (x * GRID_SIZE) + (GRID_SIZE // 2)
        y = (y * GRID_SIZE) + (GRID_SIZE // 2)
        source = DEATH_SPRITE + '.png'
        super().__init__(x=x,y=y,source=source,format=(2,4))
        self.frame = 0
        self.hitbox = None

    def deathAnimation(self,dt):
        """
        Animates the death of the frog

        Parameter dt: The time in seconds since last update
        Precondition: dt is an int or a float
        """
        self._deathSound.play()
        self._animating = True
        self._time = 0

        while self._animating:
            dt = (yield)
            self._time += dt
            duration = DEATH_SPEED

            currentFrame = round(8 * (self._time/duration))
            self.frame = currentFrame
            if self._time >= duration:
                self.frame = 8
                self._animating = False
