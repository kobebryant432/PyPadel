class Point:
    cat = {"f": "Forced Winner", "u": "Unforced Error", "w": "Winner"}
    side = {"fh": "Forehand", "bh": "Backhand", "hi": "High", "hd": "High defense"}
    shot = {
        "v": "Volley",
        "o": "Other",
        "n": "Normal",
        "g": "Glass",
        "r": "return",
        "l": "lob",
        "s": "smash",
        "V": "vibora",
        "k": "kick",
        "b": "bandeja",
        "j": "bajada",
        "f": "fake",
        "z": "double fault",
    }
    direction = {
        "c": "cross",
        "p": "parallel",
        "n": "net",
        "l": "long",
        "m": "middle",
        "d": "dropshot",
        "k": "dunk",
        "g": "globo",
        "f": "fence",
    }

    # New reverse shot dictionary
    reverse_shot = {value: key for key, value in shot.items()}

    def __init__(self, string) -> None:
        # Initialize all attributes with None or default values
        self.player = None
        self.category = None
        self.side = None
        self.shot_type = None
        self.direction = None

        # Look for the player identifier
        if string[0] == "#":
            self.player = int(string[1])
        else:
            self.player = int(string[0])
            self.category = Point.cat[string[1]]
            self.side = Point.side[string[2:4]]
            # Handle shot type
            if string[2:4] in ["hi", "hd"] and string[4] == "v":
                self.shot_type = self.shot["V"]
            else:
                if string[4] not in self.shot:
                    if string[4:] in self.reverse_shot:
                        self.shot_type = string[4:]
                    else:
                        raise ValueError(f"Invalid shot type: {string[4:]}")
                else:
                    self.shot_type = self.shot[string[4]]
            self.direction = Point.direction[string[5]]

        # raw string
        self.raw = string

    def __str__(self) -> str:
        return f"Player {self.player} made a {self.category} on a {self.side} {self.shot_type} in the {self.direction}"


class Winner(Point):
    def __init__(self, string) -> None:
        super().__init__(string)


class Unforced_error(Point):
    def __init__(self, string) -> None:
        super().__init__(string)


class Forced_winner(Point):
    def __init__(self, string) -> None:
        super().__init__(string)
        self.player2 = string[6]
        self.side2 = string[7:9]
        self.shot_type_2 = string[9]
