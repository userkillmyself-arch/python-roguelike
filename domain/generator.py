import argparse
import os
import random
from collections import deque

# параметры 
WIDTH, HEIGHT = 60, 22         
ROOMS = 9                     
ROOM_MIN_W, ROOM_MIN_H = 6, 4

ENEMIES_START = 3
ENEMIES_STEP = 2
ITEMS_MIN, ITEMS_MAX = 2, 4

# название, class в items-файле, диапазон стоимости
ITEM_CATALOG = [
    ("Сокровища", "treasures", (8, 20)),
    ("Зелье здоровья", "heal", (5, 5)),
]

WALL, FLOOR = '0', '1'
MIN_LEAF_W = ROOM_MIN_W + 2
MIN_LEAF_H = ROOM_MIN_H + 2


# BSP 
class Leaf:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.left = self.right = None
        self.room = None

    def split(self):
        can_v = self.w >= 2 * MIN_LEAF_W
        can_h = self.h >= 2 * MIN_LEAF_H
        if not (can_v or can_h):
            return False
        if can_v and can_h:
            vertical = self.w / self.h > 1.25 or (
                self.h / self.w <= 1.25 and random.random() < 0.5)
        else:
            vertical = can_v
        if vertical:
            cut = random.randint(MIN_LEAF_W, self.w - MIN_LEAF_W)
            self.left = Leaf(self.x, self.y, cut, self.h)
            self.right = Leaf(self.x + cut, self.y, self.w - cut, self.h)
        else:
            cut = random.randint(MIN_LEAF_H, self.h - MIN_LEAF_H)
            self.left = Leaf(self.x, self.y, self.w, cut)
            self.right = Leaf(self.x, self.y + cut, self.w, self.h - cut)
        return True

    def rooms(self):
        if self.room:
            return [self.room]
        return self.left.rooms() + self.right.rooms()


def build_tree():
    root = Leaf(0, 0, WIDTH, HEIGHT)
    leaves = [root]
    while len(leaves) < ROOMS:
        for leaf in sorted(leaves, key=lambda l: l.w * l.h, reverse=True):
            if leaf.split():
                leaves.remove(leaf)
                leaves += [leaf.left, leaf.right]
                break
        else:
            return None, None         # больше резать некуда
    return root, leaves


def make_room(leaf):
    rw = random.randint(ROOM_MIN_W, leaf.w - 2)
    rh = random.randint(ROOM_MIN_H, leaf.h - 2)
    rx = random.randint(leaf.x + 1, leaf.x + leaf.w - rw - 1)
    ry = random.randint(leaf.y + 1, leaf.y + leaf.h - rh - 1)
    leaf.room = (rx, ry, rw, rh)


def center(room):
    x, y, w, h = room
    return x + w // 2, y + h // 2


def carve_room(grid, room):
    x, y, w, h = room
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            grid[yy][xx] = FLOOR


def carve_corridor(grid, a, b):
    (x1, y1), (x2, y2) = a, b
    if random.random() < 0.5:
        corner = (x2, y1)             # сначала по горизонтали
    else:
        corner = (x1, y2)             # сначала по вертикали
    for (sx, sy), (ex, ey) in ((a, corner), (corner, b)):
        for yy in range(min(sy, ey), max(sy, ey) + 1):
            for xx in range(min(sx, ex), max(sx, ex) + 1):
                grid[yy][xx] = FLOOR


def connect(grid, node):
    if node.room:
        return
    connect(grid, node.left)
    connect(grid, node.right)
    a = random.choice(node.left.rooms())
    b = random.choice(node.right.rooms())
    carve_corridor(grid, center(a), center(b))


# проверки
def bfs(grid, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in dist and grid[n[1]][n[0]] != WALL:
                dist[n] = dist[(x, y)] + 1
                queue.append(n)
    return dist


def is_connected(grid, rooms):
    dist = bfs(grid, center(rooms[0]))
    floor = sum(c != WALL for row in grid for c in row)
    return len(dist) == floor and all(center(r) in dist for r in rooms)


#наполнение 
def room_cells(room):
    x, y, w, h = room
    return [(xx, yy) for yy in range(y, y + h) for xx in range(x, x + w)]


def enemy_count(level):
    return ENEMIES_START + ENEMIES_STEP * (level - 1)


def pick_enemy(level):
    vampire_chance = min(0.6, 0.1 + 0.15 * (level - 1))
    return 'V' if random.random() < vampire_chance else 'Z'


def generate_level(level, total):
    while True:
        root, leaves = build_tree()
        if root is None:
            continue
        for leaf in leaves:
            make_room(leaf)
        grid = [[WALL] * WIDTH for _ in range(HEIGHT)]
        rooms = root.rooms()
        for room in rooms:
            carve_room(grid, room)
        connect(grid, root)
        if len(rooms) == ROOMS and is_connected(grid, rooms):
            break

    start_room = random.choice(rooms)
    sx, sy = center(start_room)
    grid[sy][sx] = 'S'

    # выход в самой далёкой комнате
    dist = bfs(grid, (sx, sy))
    others = [r for r in rooms if r != start_room]
    exit_room = max(others, key=lambda r: dist[center(r)])
    ex, ey = center(exit_room)
    grid[ey][ex] = 'F' if level == total else 'X'

    # враги и предметы только вне стартовой комнаты
    free = [c for r in others for c in room_cells(r) if c != (ex, ey)]
    random.shuffle(free)

    for _ in range(min(enemy_count(level), len(free))):
        x, y = free.pop()
        grid[y][x] = pick_enemy(level)

    items = []
    for _ in range(min(random.randint(ITEMS_MIN, ITEMS_MAX), len(free))):
        x, y = free.pop()
        grid[y][x] = 'i'
        name, cls, (lo, hi) = random.choice(ITEM_CATALOG)
        items.append((name, cls, random.randint(lo, hi)))

    return [''.join(row) for row in grid], items, rooms


# запись
def write_level(out, n, rows, items):
    with open(os.path.join(out, f"map{n}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    with open(os.path.join(out, f"map{n}_items.txt"), "w", encoding="utf-8") as f:
        for name, cls, cost in items:
            f.write(f"{name}:\nclass = {cls}\ncost = {cost}\n\n")


DEFAULT_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levels")

def generate_all(levels=5, out=DEFAULT_OUT, seed=None):
    if seed is not None:
        random.seed(seed)
    os.makedirs(out, exist_ok=True)
    for n in range(1, levels + 1):
        rows, items, _ = generate_level(n, levels)
        write_level(out, n, rows, items)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", type=int, default=5)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()
    generate_all(args.levels, args.out, args.seed)


if __name__ == "__main__":
    main()
