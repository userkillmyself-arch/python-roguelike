class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Game:
    def __init__(self, load_level):
        self.load_level = load_level
        self.level = 1
        self.finished = False
        self.player = Player()
        self.tiles = load_level(self.level)
        self._place_player()

    def find(self, char):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == char:
                    return x, y
        raise ValueError(f"на уровне {self.level} нет клетки '{char}'")

    def _place_player(self):
        self.player.x, self.player.y = self.find('S')

    def next_level(self):
        tiles = self.load_level(self.level + 1)
        if tiles is None:
            self.finished = True  # уровни закончились
            return
        self.level += 1
        self.tiles = tiles
        self._place_player()

    def is_walkable(self, x, y):
        return (0 <= y < len(self.tiles)
                and 0 <= x < len(self.tiles[y])
                and self.tiles[y][x] != '0')

    def move_player(self, dx, dy):
        nx, ny = self.player.x + dx, self.player.y + dy
        if self.is_walkable(nx, ny):
            self.player.x, self.player.y = nx, ny
            if self.tiles[ny][nx] == 'X':
                self.next_level()

