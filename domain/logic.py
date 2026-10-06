class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.health = 10


class Enemy:
    damage = 1
    radius = 6        # радиус враждебности (в клетках)
    move_every = 2    # двигаться раз в N кадров (1 = каждый кадр)

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.timer = 0


class Zombie(Enemy):
    damage = 1
    radius = 6
    move_every = 2


class Game:
    def __init__(self, load_level):
        self.load_level = load_level
        self.level = 1
        self.result = None   # None - идёт игра, 1 - победа, 0 - поражение
        self.player = Player()
        self._setup(load_level(self.level))

    def _setup(self, tiles):
        self.tiles = tiles
        self.enemies = []
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile == 'Z':
                    self.enemies.append(Zombie(x, y))
                    tiles[y][x] = '1'  # под зомби обычный пол
        self.player.x, self.player.y = self.find('S')

    def find(self, char):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == char:
                    return x, y
        raise ValueError(f"на уровне {self.level} нет клетки '{char}'")

    def next_level(self):
        tiles = self.load_level(self.level + 1)
        if tiles is None:
            return
        self.level += 1
        self._setup(tiles)

    def is_walkable(self, x, y):
        return (0 <= y < len(self.tiles)
                and 0 <= x < len(self.tiles[y])
                and self.tiles[y][x] != '0')

    def enemy_at(self, x, y):
        return any(e.x == x and e.y == y for e in self.enemies)

    def move_player(self, dx, dy):
        nx, ny = self.player.x + dx, self.player.y + dy
        if self.is_walkable(nx, ny) and not self.enemy_at(nx, ny):
            self.player.x, self.player.y = nx, ny
            tile = self.tiles[ny][nx]
            if tile == 'F':
                self.result = 1
                return
            if tile == 'X':
                self.next_level()
                return
        self._tick()

    def _tick(self):
        for e in self.enemies:
            dist = abs(e.x - self.player.x) + abs(e.y - self.player.y)

            if dist <= e.radius:
                e.timer += 1
                if e.timer >= e.move_every:
                    e.timer = 0
                    self._move_enemy(e)
            else:
                e.timer = 0   # игрок далеко, зомби стоит

            if abs(e.x - self.player.x) + abs(e.y - self.player.y) == 1:
                self.player.health -= e.damage

        if self.player.health <= 0:
            self.player.health = 0
            self.over = True

        if self.player.health <= 0:
            self.player.health = 0
            self.result = 0

    def _move_enemy(self, e):
        px, py = self.player.x, self.player.y
        dx = (px > e.x) - (px < e.x)
        dy = (py > e.y) - (py < e.y)
        if abs(px - e.x) >= abs(py - e.y):
            options = [(dx, 0), (0, dy)]
        else:
            options = [(0, dy), (dx, 0)]
        for ox, oy in options:
            nx, ny = e.x + ox, e.y + oy
            if (ox, oy) != (0, 0) and self.is_walkable(nx, ny) \
                    and not self.enemy_at(nx, ny) and (nx, ny) != (px, py):
                e.x, e.y = nx, ny
                break

