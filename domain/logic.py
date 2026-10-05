class Player:
    def __init__(self):
        self.x = 2
        self.y = 2

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class MapSize:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def ask_map_size():
    print("введи размер карты")
    x = int(input())
    y = int(input())
    return MapSize(x, y)


if __name__ == "__main__":
    import view
    view.run()


