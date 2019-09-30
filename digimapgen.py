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
version = "0.2.2"
#Amount of generators.
gencount = 1
#Maximum tileset ID.
tilemax = 5
#Move types.
ROW = 1
COL = 2
#Tileset indicies.
ID  = 0
FILL = 1
OUTLINE = 2
TEXT = 3
TEXTCOLOR = 4
#ROW and SQ.
ROW = 0
SQ = 1

#Tileset.
tileset = {
'MISSINGNO' : [0, '#a832a6', '#330e32', '?', '#ffffff'],
'GRASS' : [1, '#14a333', '#2e1a03', None, None],
'WATER' : [2, '#19cbd1', '#19cbd1', None, None],
'SAND' : [3, '#fff373', '#ffce52', None, None],
'TREE' : [4, '#14a333', '#2e1a03', '\uD83C\uDF32', '#2e1a03'], #Unicode character: 🌲
'BLACK' : [5, '#000000', '#ffffff', None, None]
}

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
    generate(settings['generator'])
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
    delay = turtle.numinput('DigiMapGen', 'Set animation delay:', 0.1)
    if delay <= 0:
        turtle.tracer(False)
        turtle.delay(delay)
        turtle.speed(0)
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

def chooseTile(n):
#Get tile key from tile ID.
    if n > tilemax: return 'MISSINGNO'
    elif n == tileset['MISSINGNO'][ID]: return 'MISSINGNO'
    elif n == tileset['GRASS'][ID]: return 'GRASS'
    elif n == tileset['WATER'][ID]: return 'WATER'
    elif n == tileset['SAND'][ID]: return 'SAND'
    elif n == tileset['TREE'][ID]: return 'TREE'
    elif n == tileset['BLACK'][ID]: return 'BLACK'
    else: return 'MISSINGNO'

def drawTile(tile):
#Draw a tile.
    currenttile = chooseTile(tile)
    currentfill = tileset[currenttile][FILL]
    currentoutline = tileset[currenttile][OUTLINE]
    currenttext = tileset[currenttile][TEXT]
    currenttextcolor = tileset[currenttile][TEXTCOLOR]
    istext = False if tileset[currenttile][TEXT] is None else True
    turtle.color(currentoutline, currentfill)
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
    if istext: printTextInTile(currenttext, currenttextcolor)

def printTextInTile(text, color):
#Adds text to a tile [please don't send more than one character.]
    currentheading = turtle.heading()
    turtle.up()
    turtle.seth(direct['SOUTH'])
    turtle.forward(settings['tilesize'])
    turtle.seth(direct['EAST'])
    turtle.forward(settings['tilesize'] / 2)
    turtle.color(color)
    turtle.write(text, False, "center", ("Arial", int(settings['tilesize'] / 1.5), "bold"))
    turtle.seth(direct['WEST'])
    turtle.forward(settings['tilesize'] / 2)
    turtle.seth(direct['NORTH'])
    turtle.forward(settings['tilesize'])
    turtle.seth(currentheading)

def drawMap():
#Draw the whole map.
    currentrow = 0
    currentsquare = 0
    for row in map:
        currentsquare = 0
        currentrow += 1
        for i in row:
            currentsquare += 1
            logger.msg(f"Drawing tile: ({currentrow}, {currentsquare}) {i}/{chooseTile(i)}")
            drawTile(i)
            move(ROW)
        move(COL)
    turtle.tracer(True)
    turtle.hideturtle()
    turtle.done()

def debugInfo():
#Print some info about the map.
    logger.msg(f"Window size: {conf.windowsize}%")
    logger.msg(f"Window width: {turtle.window_width()}px")
    logger.msg(f"Map width: {settings['mapwidth']}")
    logger.msg(f"Tile size: {settings['tilesize']}")

def generate(n):
#Splits off into various generator functions.
    if n > gencount: return
    elif n == 0: gen0()
    elif n == 1: gen1()
    else: return

def gen0():
#Generator 0: Plain grid
    tilechoice = int(turtle.numinput('DigiMapGen', 'What tile?:', 0, 0, tilemax))
    global map
    map = [[tilechoice] * settings['mapwidth']] * settings['mapwidth']
    for row in map:
        logger.load(row)

def gen1():
#Generator 1: Overworld
    global map

    #Fill the map with grass.
    map = [[tileset['GRASS'][ID]] * settings['mapwidth']] * settings['mapwidth']

    #LAKE GEN
    #Dot lakes across the map.
    lakes = []
    for row in range(0, settings['mapwidth'] - 1):
        for sq in range(0, settings['mapwidth'] - 1):
            if random.randint(1, 20) == 1:
                map[row][sq] = tileset['WATER'][ID]
                lakes.append([row, sq])

    #Print the finished map.
    for row in map:
        logger.load(row)

#Main loop.
try:
    main()
except turtle.Terminator:
    logger.crit("Program terminated early!")
