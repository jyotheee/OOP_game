import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
BUG = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Girl"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y - 1)
        elif direction == "down":
            return (self.x, self.y + 1)
        elif direction == "left":
            return (self.x - 1, self.y)
        elif direction == "right":
            return (self.x + 1, self.y)
        return None

# eventually we will include different-colored gems and assign different point values to them
class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class Bug(GameElement):
    IMAGE = "Bug"

    # To include: Disable the keyboard control for the player because the game is over
    def interact(self, player):
        GAME_BOARD.draw_msg("You were eaten by a bug!")
        GAME_BOARD.del_el(player.x, player.y)

    # bug moves when player moves
    def move(self, player):
        next_x = None
        next_y = None

        print "Bug moved"

        if player.x > self.x:
            next_x = self.x + 1
            next_y = self.y
        elif player.y < self.y:
            next_x = self.x
            next_y = self.y - 1
        elif player.x < self.x:
            next_x = self.x - 1
            next_y = self.y
        elif player.y > self.y:
            next_x = self.x
            next_y = self.y + 1

        if next_x == GAME_WIDTH or next_x < 0 or next_y == GAME_HEIGHT or next_y < 0:
            print "Cannot move outside the boundary."
            GAME_BOARD.draw_msg("Bug cannot move outside the boundary")
        else:
            next_element = GAME_BOARD.get_el(next_x, next_y)
            if next_element is None or not next_element.SOLID:
                GAME_BOARD.del_el(self.x, self.y)
                GAME_BOARD.set_el(next_x, next_y, self)
                if next_x == player.x and next_y == player.y:
                    print "You got eaten"
                    GAME_BOARD.draw_msg("Game Over! Player eaten by the bug")
                    GAME_BOARD.gameover = True


class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player):
        # the player's inventory will become the chest's inventory
        pass


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    # obstacle rocks
    rock_positions = [(3,4), (1,5), (2,6), (4,1)]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    rocks[-1].SOLID = False

    # create a player
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(GAME_WIDTH/2, GAME_HEIGHT/2, PLAYER)
    print PLAYER

    # draw a board
    GAME_BOARD.draw_msg("This game is the best.")

    # create a chest at the bottom right hand corner
    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(GAME_WIDTH-1, GAME_HEIGHT-1, chest)
    print "Chest created at the bottom right hand corner"

    # create three gems in random locations, first checking that the location is empty
    gems = []
    gemcounter = 0

    while gemcounter < 3:
            gem = Gem()
            GAME_BOARD.register(gem)
            location = (random.randint(0, 4), random.randint(0,4))
            object_at_location = GAME_BOARD.get_el(location[0], location[1])
            if object_at_location == None:
                GAME_BOARD.set_el(location[0], location[1], gem)
                print "This space contains %r, creating new gem" % object_at_location
                gems.append(gem)
                gemcounter += 1

    # create bugs at random locations
    global BUG
    BUG = Bug()
    GAME_BOARD.register(BUG)
    GAME_BOARD.set_el(1, 1, BUG)

def keyboard_handler():
    direction = None
  
    if GAME_BOARD.gameover == True:
       direction = None
    elif KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()

    next_x = None
    next_y = None

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

    if next_x == GAME_WIDTH or next_x < 0 or next_y == GAME_HEIGHT or next_y < 0:
        GAME_BOARD.draw_msg("Cannot move outside the boundary.")
    else:
        GAME_BOARD.draw_msg("next_x: %r and next_y: %r" % (next_x, next_y) )        
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(PLAYER)
 
        # if isinstance(existing_el, Bug):
        #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        #     GAME_BOARD.set_el(next_x, next_y, existing_el)
        #     print "You got eaten by a bug!"
        #     GAME_BOARD.gameover = True
        
        # defines how a player moves in the game board    
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
            BUG.move(PLAYER)

    if GAME_BOARD.gameover == True:
        GAME_BOARD.draw_msg("GAME OVER: BUG EATS GIRL")