class Point:
    """Class to represent a point in a game.

    Parameters
    ----------
    string : str
        A string containing information about the point.

    Attributes
    ----------
    player : int
        The player number associated with the point.
    category : str
        The category of the last shot of the point.
    side : str
        The side where the last shot of the point was played.
    shot_type : str
        The type shot the the last shot of the point was.
    direction : str
        The direction of the last shot of the point.
    raw : str
        The raw string representation of the point.

    Notes
    -----
    - This class is designed to process a specific format of string input to extract information about a point in a game.
    - The `cat`, `side`, `shot`, and `direction` attributes are dictionaries mapping specific codes to their corresponding values.
    - If the shot type is not found in the `shot` dictionary, a ValueError is raised.
    """

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

    def __init__(self, string: str) -> None:
        """
        Initialize a Point object from a string.

        Parameters
        ----------
        string : str
            A string containing information about the end of the point.
        """

        self.player = int(string[1])
        self.category = Point.cat[string[2]]
        self.side = Point.side[string[3:5]]

        # Dubbel use of letter v -> if high v than it is a Vibora (V) else it is a volley (v)
        if string[3:5] in ["hi", "hd"] and string[5] == "v":
            self.shot_type = self.shot["V"]
        else:
            # If the shot type from string is not in shot dictionary
            if string[5] not in self.shot:
                if string[5:] in self.reverse_shot:
                    self.shot_type = string[5:]
                else:
                    raise ValueError(f"Invalid shot type: {string[4:]}")
            else:
                self.shot_type = self.shot[string[5]]

        self.direction = Point.direction[string[6]]
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
        self.player2 = string[7]
        self.side2 = string[8:10]
        self.shot_type_2 = string[10]
