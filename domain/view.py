import curses
from logic import Game
from map import load_map

KEYS = {
    curses.KEY_UP: (0, -1),
    curses.KEY_DOWN: (0, 1),
    curses.KEY_LEFT: (-1, 0),
    curses.KEY_RIGHT: (1, 0),
}

FRAME_COLOR = 2  # пара цветов, можно завести отдельную

def draw_frame(screen, h, w):
    screen.addstr(0, 0, '╔' + '═' * w + '╗', curses.color_pair(FRAME_COLOR))
    for y in range(1, h + 1):
        screen.addstr(y, 0, '║', curses.color_pair(FRAME_COLOR))
        screen.addstr(y, w + 1, '║', curses.color_pair(FRAME_COLOR))
    screen.addstr(h + 1, 0, '╚' + '═' * w + '╝', curses.color_pair(FRAME_COLOR))



def draw(screen, game):
    screen.clear()
    h = len(game.tiles)
    w = len(game.tiles[0])

    draw_frame(screen, h, w)
    screen.addstr(h + 3, 0, "↑ ↓ ← → Q")
    screen.addstr(h + 5, 0, f"position: ({game.player.x}, {game.player.y})")

    for y, row in enumerate(game.tiles):
        for x, tile in enumerate(row):
            if (x, y) == (game.player.x, game.player.y):
                screen.addch(y + 1, x + 1, '█')
            elif tile == '0':
                screen.addch(y + 1, x + 1, '█', curses.color_pair(1))
            elif tile == 'X':
                screen.addch(y + 1, x + 1, 'X', curses.color_pair(1))
            else:
                screen.addch(y + 1, x + 1, ' ')

    screen.refresh()

def main(screen):
    curses.start_color()
    curses.init_pair(1, 208, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    screen.keypad(True)
    curses.curs_set(0)

    game = Game(load_map)

    while True:
        draw(screen, game)
        if game.finished:
            break
        key = screen.getch()
        if key in KEYS:
            game.move_player(*KEYS[key])
        elif key == ord('q'):
            break
    return game

def run():
    game = curses.wrapper(main)
    print(f"position: ({game.player.x}, {game.player.y})")