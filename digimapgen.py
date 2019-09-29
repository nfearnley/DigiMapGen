import turtle
import random

import digilogger as logger
import conf

#Constants.
#Define cardinal directions.
direct = {
    'NORTH': 90,
    'EAST': 0,
    'SOUTH': 270,
    'WEST': 180}
#Current version number.
version = "0.1.0"
#Amount of generators.
gencount = 1
#Move types.
ROW = 1
COL = 2

#Settings.
settings = {
    'mapwidth' : 10,
    'generator' : 0,
    'tilesize' : 10
}

#Global variables.
#Loaded map.
map = [[]]
#Window dimensions.
monitorheight = 600
monitorwidth = 800

def main():
#Main loop.
    turtle.title(f"DigiMapGen v{version}")
    turtle.home()
    chooseSettings()
    debugInfo()
    goToStart()
    turtle.color('white', 'black') #Debug only.
    gen0()
    drawMap()

def getMonitorDimensions():
#Hacky way to get the current monitor resolution.
    global monitorheight, monitorwidth
    turtle.setup(1.0, 1.0)
    monitorheight = turtle.window_height()
    monitorwidth = turtle.window_width()

def chooseSettings():
#Get user input to determine to settings.
    global settings
    #Ask the user which generator they want to use.
    gen = turtle.numinput('DigiMapGen', 'Input a generator number:', 0, minval = 0, maxval = gencount)
    #Make sure the user put in a real generator.
    if gen in range(gencount + 1): settings['generator'] = gen
    else:
        logger.warn('ERROR: Invalid generator.')
        chooseSettings()
    #Ask the user how many tiles across they want the map to be.
    settings['mapwidth'] = int(turtle.numinput('DigiMapGen', 'Set map width:', 10))
    #Get animation delay from user.
    delay = turtle.numinput('DigiMapGen', 'Set animation delay:', 0)
    if delay <= 0:
        turtle.tracer(None)
        turtle.delay(delay)
    else:
        turtle.delay(delay)
    #Get the window size from the config.
    if conf.windowsize / 100 > 1: winsize = 1
    else: winsize = conf.windowsize / 100
    getMonitorDimensions()
    turtle.setup(monitorheight * winsize, monitorheight * winsize)
    #Determine tile size using math.
    settings['tilesize'] = (turtle.window_height() * 0.9) / settings['mapwidth']

def goToStart():
#Go to the top left of the map.
#Makes maps more or less centered.
    turtle.up()
    topleft = ((settings['mapwidth'] * settings['tilesize']) / 2) #Row width * tile size in px, halfed.
    turtle.setpos (-topleft, topleft)
    turtle.down()
    logger.msg(f"Start location: -{topleft}, {topleft}")

def move(type):
#Move the turtle to the next tile location.
    if type == ROW:
        turtle.up()
        turtle.seth(direct['EAST'])
        turtle.forward(settings['tilesize'])
    elif type == COL:
        turtle.up()
        turtle.seth(direct['SOUTH'])
        turtle.forward(settings['tilesize'])
        turtle.seth(direct['WEST'])
        turtle.forward(settings['tilesize'] * settings['mapwidth'])
    else: return

def drawTile():
#Draw a tile.
    turtle.down()
    turtle.begin_fill()
    turtle.seth(direct['EAST'])
    turtle.forward(settings['tilesize'])
    turtle.seth(direct['SOUTH'])
    turtle.forward(settings['tilesize'])
    turtle.seth(direct['WEST'])
    turtle.forward(settings['tilesize'])
    turtle.seth(direct['NORTH'])
    turtle.forward(settings['tilesize'])
    turtle.end_fill()
    turtle.up()

def drawMap():
#Draw the whole map.
    for i in map:
        for j in map:
            drawTile()
            move(ROW)
        move(COL)
    turtle.hideturtle()
    turtle.done()

def debugInfo():
#Print some info about the map.
    logger.msg(f"Window size: {conf.windowsize}%")
    logger.msg(f"Window width: {turtle.window_width()}px")
    logger.msg(f"Map width: {settings['mapwidth']}")
    logger.msg(f"Tile size: {settings['tilesize']}")

def gen0():
#Generator 0: Plain grid
    global map
    #map = [[] * settings['mapwidth']]
    #for i in range(settings['mapwidth']):
    #    for j in range(settings['mapwidth']):
    #        map[i][j] = 0
    map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

#Main loop.
main()
