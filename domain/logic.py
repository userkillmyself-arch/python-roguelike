class Player:
    def __init__(self):
        self.x = 2
        self.y = 2

    def move(self, dx, dy):
        self.x += dx
        self.y += dy





if __name__ == "__main__":
    import view
    view.run()


