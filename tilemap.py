from utils import enumerate2d
from tileset import tileset


class TileMap:
    def __init__(self, width):
        self.width = width
        self._rows = []
        for _ in range(self.width):
            row = [tileset.missing.id] * self.width
            self._rows.append(row)

    def __getitem__(self, coords):
        x, y = coords
        return self._rows[x][y]

    def __setitem__(self, coords, val):
        x, y = coords
        self._rows[x][y] = val

    def fill(self, tileid):
        for x, y, _ in enumerate2d(self):
            self[x, y] = tileid

    def __iter__(self):
        return iter(self._rows)

    def __str__(self):
        return "\n".join(str(row) for row in self._rows)
