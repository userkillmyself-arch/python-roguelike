import curses

class player:
    player_x = 0
    player_y = 0

screen = curses.initscr()
screen.keypad(True)
curses.noecho()

gamer = player()
while True:
    screen.clear()
    screen.addch(gamer.player_y, gamer.player_x, '@')
    screen.refresh()

    key = screen.getch()
    if key == curses.KEY_UP:
        gamer.player_y = gamer.player_y - 1
    elif key == curses.KEY_DOWN:
        gamer.player_y = gamer.player_y + 1
    elif key == curses.KEY_LEFT:
        gamer.player_x = gamer.player_x - 1
    elif key == curses.KEY_RIGHT:
        gamer.player_x = gamer.player_x + 1
    elif key == ord('q'):
        break

curses.endwin()
print(f"Player position: ({gamer.player_x}, {gamer.player_y})")