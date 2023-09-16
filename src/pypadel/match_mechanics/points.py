from .point_mappings import cat, side, shot, direction, POINT_STRUCTURE, FORCED_WINNER_POINT_STRUCTURE
import random

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

    # Use the imported dictionaries
    cat = cat
    side = side
    shot = shot
    direction = direction
    POINT_STRUCTURE = POINT_STRUCTURE

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

        self.player = int(string[POINT_STRUCTURE['player']])
        self.category = Point.cat[string[POINT_STRUCTURE['category']]]
        self.side = Point.side[string[POINT_STRUCTURE['side']]]

        # Dubbel use of letter v -> if high v than it is a Vibora (V) else it is a volley (v)
        if string[POINT_STRUCTURE['side']] in ["hi", "hd"] and string[POINT_STRUCTURE['shot_type']] == "v":
            self.shot_type = self.shot["V"]
        else:
            # If the shot type from string is not in shot dictionary
            if string[POINT_STRUCTURE['shot_type']] not in self.shot:
                if string[POINT_STRUCTURE['shot_type']:] in self.reverse_shot:
                    self.shot_type = string[POINT_STRUCTURE['shot_type']:]
                else:
                    raise ValueError(f"Invalid shot type: {string[POINT_STRUCTURE['shot_type']]}")
            else:
                self.shot_type = self.shot[string[POINT_STRUCTURE['shot_type']]]

        self.direction = Point.direction[string[POINT_STRUCTURE['direction']]]
        self.raw = string

    def __str__(self) -> str:
        return f"Player {self.player} made a {self.category} on a {self.side} {self.shot_type} in the {self.direction}"

    @staticmethod
    def generate_valid_point_strings():
        valid_point_strings = set()
        for player in range(1, 5):
            for cat_key in Point.cat.keys():
                for side_key in Point.side.keys():
                    for shot_key in Point.shot.keys():
                        for direction_key in Point.direction.keys():
                            # Generate additional point strings for forced winners
                            if cat_key == "f":
                                # Introduce a probability to limit the number of forced winners
                                if random.random() < 0.5:
                                    for player2 in range(1, 5):
                                        if player2 != player:  # Ensure the second player is not the same as the first player
                                            for side2_key in Point.side.keys():
                                                for shot2_key in Point.shot.keys():
                                                    valid_point_strings.add(str(player) + cat_key + side_key + shot_key + direction_key + str(player2) + side2_key + shot2_key)
                            else:
                                # Generate point strings for all categories, not just forced winners
                                valid_point_strings.add(str(player) + cat_key + side_key + shot_key + direction_key)                        
        # Adjust the distribution of point strings in the final set
        forced_winner_strings = [point_string for point_string in valid_point_strings if point_string[1] == "f"]
        unforced_error_strings = [point_string for point_string in valid_point_strings if point_string[1] == "u"]
        winner_strings = [point_string for point_string in valid_point_strings if point_string[1] == "w"]
        random.shuffle(forced_winner_strings)
        random.shuffle(unforced_error_strings)
        random.shuffle(winner_strings)
        valid_point_strings = set(forced_winner_strings[:1900] + unforced_error_strings[:1872] + winner_strings[:1872])
        return valid_point_strings



class Winner(Point):
    def __init__(self, string) -> None:
        super().__init__(string)


class Unforced_error(Point):
    def __init__(self, string) -> None:
        super().__init__(string)


class Forced_winner(Point):
    def __init__(self, string) -> None:
        super().__init__(string)
        self.player2 = int(string[FORCED_WINNER_POINT_STRUCTURE['player2']])
        self.side2 = Point.side[string[FORCED_WINNER_POINT_STRUCTURE['side2']]]
        self.shot_type_2 = Point.shot[string[FORCED_WINNER_POINT_STRUCTURE['shot_type_2']]]



