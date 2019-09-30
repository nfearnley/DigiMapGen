from turtle import Screen, Turtle

import conf
import digilogger as logger
from tileset import tileset

screen = Screen()
turtle = Turtle()

# Current version number
version = "0.2.2"

# Constants
# Define cardinal directions
NORTH = 270
EAST = 0
SOUTH = 90
WEST = 180


# Hacky way to get the current monitor resolution
def getMonitorDimensions():
    screen.setup(1.0, 1.0)
    monitorheight = screen.window_height()
    monitorwidth = screen.window_width()
    return monitorheight, monitorwidth


class TileMapDisplay:
    def __init__(self, tilemap, speed=None):
        self._tilemap = tilemap
        if speed is not None:
            self.setSpeed(speed)

        screen.title(f"DigiMapGen v{version}")
        turtle.home()

        # Get the window size from the config, anything over 100% is set to 1
        winsize = min(conf.windowsize / 100, 1)

        # Get monitor dimension, and determine the length of the smallest side
        monitorheight, monitorwidth = getMonitorDimensions()
        monitorside = min(monitorheight, monitorwidth)

        # Set window size
        # Make sure dimensions are ints, so turtle displays window in pixels, not percentage
        screen.setup(int(monitorside * winsize), int(monitorside * winsize))

        # Calculate coordinate size of borders, assuming tilemap takes 90% of the display
        tilecount = self._tilemap.width
        borderCoords = (tilecount / 9) / 2

        left = -borderCoords
        bottom = tilecount + borderCoords
        right = tilecount + borderCoords
        top = -borderCoords

        # Special coordinate system
        # (0,0) is the top-left of the displayed tilemap
        # (tilecount,tilecount) is the bottom-right of the displayed tilemap
        # Leaves space for 5% border on each side
        screen.setworldcoordinates(left, bottom, right, top)

        tilesize = monitorside / tilecount
        self.fontsize = int(tilesize / 1.5)

        turtle.color("white", "black")  # Debug only

    # Draw the whole map
    def draw(self):
        for y, row in enumerate(self._tilemap):
            for x, tileid in enumerate(row):
                logger.msg(f"Drawing tile: ({x}, {y}) {tileid}/{tileset[tileid].name}")
                tile = tileset[tileid]
                self.drawTile(tile)
                self.gotoNextCol()
            self.gotoNextRow()
        screen.tracer(True)
        turtle.hideturtle()
        screen.mainloop()

    # Move the turtle to the next tile location
    def gotoNextCol(self):
        turtle.up()
        turtle.seth(EAST)
        turtle.forward(1)

    # Move the turtle to the next tile location
    def gotoNextRow(self):
        turtle.up()
        turtle.seth(SOUTH)
        turtle.forward(1)
        turtle.seth(WEST)
        turtle.forward(self._tilemap.width)

    # Draw a tile
    def drawTile(self, tile):
        turtle.color(tile.outline, tile.fill)
        turtle.down()
        turtle.begin_fill()
        turtle.seth(EAST)
        turtle.forward(1)
        turtle.seth(SOUTH)
        turtle.forward(1)
        turtle.seth(WEST)
        turtle.forward(1)
        turtle.seth(NORTH)
        turtle.forward(1)
        turtle.end_fill()
        if tile.text:
            self.drawTileText(tile.text, tile.textcolor)

    # Adds text to a tile (only prints first character)
    def drawTileText(self, text, color):
        char = text[0:1]  # Get first character
        currentheading = turtle.heading()
        turtle.up()
        turtle.seth(SOUTH)
        turtle.forward(1)
        turtle.seth(EAST)
        turtle.forward(0.5)
        turtle.color(color)
        turtle.write(char, False, "center", ("Arial", self.fontsize, "bold"))
        turtle.seth(WEST)
        turtle.forward(0.5)
        turtle.seth(NORTH)
        turtle.forward(1)
        turtle.seth(currentheading)

    def setSpeed(self, speed):
        if speed == "instant":
            screen.tracer(False)
        else:
            turtle.speed(speed)
