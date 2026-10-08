import curses
from logic import Game
from map import load_map, load_items
import view

def main():
    game = Game(load_map, load_items)
    curses.wrapper(view.run, game)

if __name__ == "__main__":
    main()