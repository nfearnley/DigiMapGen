class Tile:
    def __init__(self, name, tileid, fill, outline, text, textcolor):
        self.name = name
        self.id = tileid
        self.fill = fill
        self.outline = outline
        self.text = text
        self.textcolor = textcolor


# Tileset
class Tileset:
    def __init__(self, tiles):
        self._tilesById = dict()
        self._tilesByName = dict()
        for tile in tiles:
            self.addTile(tile)

    # Add a new tile to the tileset
    def addTile(self, tile):
        self._tilesById[tile.id] = tile
        self._tilesByName[tile.name] = tile

    # Remove a tile from the tileset
    def removeTile(self, tile):
        del self._tilesById[tile.id]
        del self._tilesByName[tile.name]

    # Get the tile by matching name, default to "missing" tile if name is not found
    def getByName(self, name):
        return self._tilesByName.get(name, self._tilesByName["missing"])

    # Get the tile by matching id, default to "missing" tile if id is not found
    def getById(self, tileid):
        return self._tilesById.get(tileid, self._tilesById[0])

    # Allow tileset.name to lookup tile by name
    def __getattr__(self, name):
        return self.getByName(name)

    # Allow tileset[tileid] to lookup tile by id
    def __getitem__(self, tileid):
        return self.getById(tileid)

    def keys(self):
        return self._tilesById.keys()

    def items(self):
        return self._tilesById.items()

    def __iter__(self):
        return iter(self._tilesById.values())


tileset = Tileset([
    Tile("missing", 0, "#a832a6", "#330e32", "?", "#ffffff"),
    Tile("grass", 1, "#14a333", "#2e1a03", None, None),
    Tile("water", 2, "#19cbd1", "#19cbd1", None, None),
    Tile("sand", 3, "#fff373", "#ffce52", None, None),
    Tile("tree", 4, "#14a333", "#2e1a03", "\uD83C\uDF32", "#2e1a03"),  # Unicode character: 🌲
    Tile("black", 5, "#000000", "#ffffff", None, None)
])
