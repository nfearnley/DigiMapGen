import turtle
import random

import digilogger as logger
import dialogs
from utils import enumerate2d
from tileset import tileset
from tilemapdisplay import TileMapDisplay
from tilemap import TileMap


class CancelException(Exception):
    pass


# Main loop
def main():
    try:
        generator, speed, mapwidth = chooseOptions()
        tilemap = generator(mapwidth)
    except CancelException as e:
        logger.msg(f"{e}, quitting")
        return

    display = TileMapDisplay(tilemap, speed=speed)

    try:
        display.draw()
    except turtle.Terminator:
        logger.crit("Program terminated early!")



def chooseOptions():
    # redefine generators dict as more generators are added
    generator = dialogs.chooseGenerator({"gen0": gen0, "gen1": gen1, "island": islandGen})
    if generator is None:
        raise CancelException("No generator chosen")

    mapwidth = dialogs.chooseMapwidth()
    if mapwidth is None:
        raise CancelException("No map width chosen")

    speed = dialogs.chooseSpeed()
    if speed is None:
        raise CancelException("No speed chosen")

    return generator, speed, mapwidth


# Generator 0: Plain grid
def gen0(mapwidth):
    tilemap = TileMap(mapwidth)

    # Ask the user what tile they want
    tileid = dialogs.chooseTile()
    if tileid is None:
        raise CancelException("No tile chosen")

    # Fill the map with that tile
    tilemap.fill(tileid)

    logger.load(tilemap)

    return tilemap


# Generator 1: Overworld
def gen1(mapwidth):
    tilemap = TileMap(mapwidth)

    # Fill the map with grass
    tilemap.fill(tileset.grass.id)

    # LAKE GEN
    # Dot lakes across the map
    lakes = []
    for x, y, _ in enumerate2d(tilemap):
        if random.randint(1, 20) == 1:
            tilemap[x, y] = tileset.water.id
            lakes.append([x, y])

    logger.load(tilemap)

    return tilemap

# Generator 2: Island


def islandGen(mapwidth):
    tilemap = TileMap(mapwidth)

    # Fill the map with grass
    tilemap.fill(tileset.grass.id)

    # Set the borders to water
    for x, y, _ in enumerate2d(tilemap):
        if x == 0 or x == tilemap.width - 1 or y == 0 or y == tilemap.width - 1:
            tilemap[x, y] = tileset.water.id

    logger.load(tilemap)

    return tilemap


# Main loop
if __name__ == "__main__":
    main()
