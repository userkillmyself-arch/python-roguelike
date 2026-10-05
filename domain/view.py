import curses
from logic import Player
from map import map_matrix 

def main(screen):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    screen.keypad(True)
    curses.curs_set(0)

    gamer = Player()
    while True:
        screen.clear()
        screen.addstr(len(map_matrix) + 5, 0, "↑ ↓ ← → Q")

        for y in range(len(map_matrix)):
            for x in range(len(map_matrix[y])):
                if (y, x) == (gamer.y, gamer.x):
                    screen.addch(y, x, '█')
                elif map_matrix[y][x] == '0':
                    screen.addch(y, x, '█', curses.color_pair(1))
                else:
                    screen.addch(y, x, ' ')




        screen.addch(gamer.y, gamer.x, '█')
        screen.refresh()

        key = screen.getch()
        if key == curses.KEY_UP and gamer.y > 0 and map_matrix[gamer.y - 1][gamer.x] != '0':
            gamer.move(0, -1)
        elif key == curses.KEY_DOWN and gamer.y < len(map_matrix) - 1 and map_matrix[gamer.y + 1][gamer.x] != '0':
            gamer.move(0, 1)
        elif key == curses.KEY_LEFT and gamer.x > 0 and map_matrix[gamer.y][gamer.x - 1] != '0':
            gamer.move(-1, 0)
        elif key == curses.KEY_RIGHT and gamer.x < len(map_matrix[0]) - 1 and map_matrix[gamer.y][gamer.x + 1] != '0':
            gamer.move(1, 0)
        elif key == ord('q'):
            break

    return gamer

def run():

    gamer = curses.wrapper(main)
    print(f"position: ({gamer.x}, {gamer.y})")


if __name__ == "__main__":
    run()