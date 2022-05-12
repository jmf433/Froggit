"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

John Fernandez jmf433
12/21/2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.


class Lane(object):
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    # Attribute _tile: The tile created for each lane
    # Invariant: _tile is a GTile object

    # Attribute _objs: The list containg the objects for each lane
    # Invariant: _objs is a list containing GImage objects

    def getTile(self):
        return self._tile

    def getObjs(self):
        return self._objs

    def __init__(self,level,x,hitboxes):
        """
        Initializer for lane object in froggit

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file

        Parameter x: The lane x from the bottom
        Precondition: x is an int

        Parameter hitboxes: The preloaded json file that contains the hitboxes
        for the objects in the game
        Precondition: hitboxes is a preloaded json file
        """
        #Creats the lanes for the level
        self._tile = GTile(width=(level['size'][0]*GRID_SIZE),height=GRID_SIZE,
        source=(level['lanes'][x]['type']+'.png'))
        self._tile.left = 0
        self._tile.bottom = GRID_SIZE * x

        #Creates the obstacles for each lane
        self._objs = []
        if level['lanes'][x]['type'] != 'grass':
            obj_dic = level['lanes'][x]['objects']

            for item in range(len(obj_dic)):
                xvalue = (obj_dic[item]['position'] * GRID_SIZE)  + (GRID_SIZE // 2)
                yvalue = (x * GRID_SIZE) + (GRID_SIZE // 2)
                new_obj = GImage(x=xvalue,y=yvalue, source=obj_dic[item]['type']+'.png')
                if level['lanes'][x]['type'] != 'hedge':
                    if level['lanes'][x]['speed'] < 0:
                        new_obj.angle = 180
                self._objs.append(new_obj)

        # Sets hitboxes for objs
        for obj in range(len(self._objs)):
            if self._objs[obj] != []:
                sourceKey = self._objs[obj].source[:-4]
                objHitbox = tuple(hitboxes['images'][sourceKey]['hitbox'])
                self._objs[obj].hitbox = objHitbox

    def update(self,pos,dt,level):
        """
        Update method for lane that updates the movement of the obstacles

        Parameter pos: The position of the lane in the json file
        Precondition: object is a GImage object

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        # Updating obstacles
        speed = level['lanes'][pos]['speed']
        buffer = level['offscreen']
        width = level['size'][0] * GRID_SIZE
        dist = speed*dt
        for y in range(len(self._objs)):
            self._objs[y].x += dist
            if self._objs[y].x >= (width + (buffer * GRID_SIZE)) and speed > 0:
                extra_space = self._objs[y].x - (width + (buffer * GRID_SIZE))
                self._objs[y].x = (-buffer * GRID_SIZE) + extra_space
            elif self._objs[y].x <= (-4 * GRID_SIZE) and speed < 0:
                extra_space = self._objs[y].x - (-4 * GRID_SIZE)
                self._objs[y].x = (width + (buffer * GRID_SIZE)) + extra_space

    def draw(self,view):
        """
        Draws the current lane for Froggit

        Parameter view: The window to draw the lanes on
        Precondition: view is a valid window
        """
        self._tile.draw(view)
        if self._objs != []:
            for obj in self._objs:
                obj.draw(view)


class Grass(Lane):
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass


class Road(Lane):
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    pass


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    def getObjs(self):
        """
        Getter for self._objs
        """
        return self._objs


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # Attribute _safeFrogs: A list containing all the frogs on the exits
    # Invariant: _safeFrogs is a list of GImages

    # Attribute _objs: The list containg the objects for each lane
    # Invariant: _objs is a list containing GImage objects

    # Attribute _totalExits: List containing the exits
    # Invariant: _totalExits is a list of GImages

    def getObjs(self):
        """
        Getter for self._objs
        """
        return self._objs

    def getSafeFrogs(self):
        """
        Getter for self._safeFrogs
        """
        return self._safeFrogs

    def __init__(self,level,x,hitboxes):
        """
        Initializer for Hedge

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file

        Parameter x: The lane x from the bottom
        Precondition: x is an int

        Parameter hitboxes: The preloaded json file that contains the hitboxes
        for the objects in the game
        Precondition: hitboxes is a preloaded json file
        """
        super().__init__(level,x,hitboxes)
        self._safeFrogs = []

    def reachExit(self,x,level):
        """
        Method that detects when the frog has reached an exit and blocks the exit

        Parameter x: The position in list of exit frog has reached
        Precondition: x is an int

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        xvalue = self._objs[x].x
        yvalue = self._objs[x].y
        if self._objs[x].source == 'exit.png':
            newFrog = GImage(x=xvalue,y=yvalue,source='safe.png')
            self._safeFrogs.append(newFrog)

    def opening(self,x,level):
        """
        Method that detects if there is an opening in the hedge for the
        frog to pass through

        Parameter x: The position in list of exit frog has reached
        Precondition: x is an int

        Parameter level: The loaded json file that contains infromation for the level
        Precondition: level is a preloaded json file
        """
        if self._objs[x].source == 'open.png':
            return True
        else:
            return False

    def numberOfExits(self):
        """
        Method that determines the number of exits that are in the current
        level for the frog to reach in order to win
        """
        self._totalExits = []
        for x in range(len(self._objs)):
            if self._objs[x].source == 'exit.png':
                self._totalExits.append(self._objs[x])
        return len(self._totalExits)

    def draw(self,view):
        """
        Draw method for Hedge

        Parameter view: The window to draw the objects on
        Precondition: view is a valid window
        """
        self._tile.draw(view)
        if self._objs != []:
            for obj in self._objs:
                obj.draw(view)
        if self._safeFrogs != []:
            for obj in self._safeFrogs:
                obj.draw(view)
