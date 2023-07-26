class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.matches = []

    def add_match(self, m):
        self.matches.append(m)
