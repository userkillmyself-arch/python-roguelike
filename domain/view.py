import curses
from logic import Player, ask_map_size

def main(screen, mapsize):
    screen.keypad(True)
    curses.curs_set(0)

    gamer = Player()
    while True:
        screen.clear()
        screen.addstr(0, 0, "↑ ↓ ← → Q")
        screen.addch(gamer.y, gamer.x, '@')
        screen.refresh()

        key = screen.getch()
        if key == curses.KEY_UP:
            gamer.move(0, -1)
        elif key == curses.KEY_DOWN:
            gamer.move(0, 1)
        elif key == curses.KEY_LEFT:
            gamer.move(-1, 0)
        elif key == curses.KEY_RIGHT:
            gamer.move(1, 0)
        elif key == ord('q'):
            break

    return gamer

def run():
    mapsize = ask_map_size()
    gamer = curses.wrapper(main, mapsize)
    print(f"position: ({gamer.x}, {gamer.y})")
    print(f"map size: ({mapsize.x} x {mapsize.y})")

if __name__ == "__main__":
    run()