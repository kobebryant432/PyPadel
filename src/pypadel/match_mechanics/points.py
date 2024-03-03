from .point_mappings import serve_type, player, cat, side, shot, direction, POINT_STRUCTURE, FORCED_WINNER_POINT_STRUCTURE
import random
import logging
from itertools import product

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
    serve_type = serve_type
    player = player
    cat = cat
    side = side
    shot = shot
    direction = direction
    POINT_STRUCTURE = POINT_STRUCTURE
    FORCED_WINNER_POINT_STRUCTURE = FORCED_WINNER_POINT_STRUCTURE

    # New reverse shot dictionary
    reverse_shot = {value: key for key, value in shot.items()}

    def _process_point_string(self, string: str) -> None:
        self.raw = string
        try:
            try:
                self.serve_type = string[Point.POINT_STRUCTURE['serve_type']]
            except Exception as e:
                print(
                    f"Error occurred while processing serve_type in raw point: {string}. \n"
                    f"Valid keys for serve_type are: {list(serve_type.keys())} \n"
                    f"Invalid element: {e}\n"
                )
                self.__class__ = InvalidPoint
                self.__init__(string, e)
                return

            try:
                self.player = int(string[Point.POINT_STRUCTURE['player']])
            except Exception as e:
                print(
                    f"Error occurred while processing player in raw point: {string}. \n"
                    f"Valid keys for player are: {list(player.keys())} \n"
                    f"Invalid element: {e}\n"
                )
                self.__class__ = InvalidPoint
                self.__init__(string, e)
                return

            try:
                self.category = Point.cat[string[Point.POINT_STRUCTURE['category']]]
            except Exception as e:
                print(
                    f"Error occurred while processing category in raw point: {string}. \n"
                    f"Valid keys for category are: {list(cat.keys())} \n"
                    f"Invalid element: {e}\n"
                )
                self.__class__ = InvalidPoint
                self.__init__(string, e)
                return

            try:
                self.side = Point.side[string[Point.POINT_STRUCTURE['side']]]
            except Exception as e:
                print(
                    f"Error occurred while processing side in raw point: {string}. \n"
                    f"Valid keys for side are: {list(side.keys())} \n"
                    f"Invalid element: {e}\n"
                )
                self.__class__ = InvalidPoint
                self.__init__(string, e)
                return

            # The logic for handling the "v" shot type remains the same
            if string[Point.POINT_STRUCTURE['side']] in ["hi", "hd"] and string[Point.POINT_STRUCTURE['shot_type']] == "v":
                self.shot_type = self.shot["V"]
            else:
                try:
                    self.shot_type = self.shot[string[Point.POINT_STRUCTURE['shot_type']]]
                except Exception as e:
                    print(
                        f"Error occurred while processing shot_type in raw point: {string}. \n"
                        f"Valid keys for shot_type are: {list(shot.keys())} \n"
                        f"Invalid element: {e}\n"
                    )
                    self.__class__ = InvalidPoint
                    self.__init__(string, e)
                    return

            try:
                self.direction = Point.direction[string[Point.POINT_STRUCTURE['direction']]]
            except Exception as e:
                print(
                    f"Error occurred while processing direction in raw point: {string}. \n"
                    f"Valid keys for direction are: {list(direction.keys())} \n"
                    f"Invalid element: {e}\n"
                )
                self.__class__ = InvalidPoint
                self.__init__(string, e)
                return

        except Exception as e:
            # This outer try-except block might not be necessary anymore since you're handling individual attributes.
            logging.basicConfig(filename='invalid_points.log', level=logging.INFO)
            logging.info(f"Invalid point: {string}. Error: {e}")
            self.raw = string
            print(f"General error occurred while processing point string: {string}. Error: {e}")


    @staticmethod

    # TODO: At this moment, this method is not perfect. For example:

    # Point string is incomplete: e4fgc2bh, attempting to complete it... 

    # Original string: e4fgc2bh
    # Filled string: e4fSigc2Sib
    # Completed point string: e4fSigc2Sib 

    # -> it incorrectly changes the side of the second player as opposed to adding a shot_type_2
    

    def complete_point_string(string: str) -> str:
        # Check if the point string represents a forced winner
        is_forced_winner = 'f' in string

        # Choose the correct point structure based on whether the point is a forced winner
        point_structure = Point.FORCED_WINNER_POINT_STRUCTURE if is_forced_winner else Point.POINT_STRUCTURE

        # Initialize a dictionary to store the identified information
        default_values = {"serve_type": "O", "player": "P", "category": "C", "side": "Si", "shot_type": "S", "direction": "D", "player2": "P", "side2": "Si", "shot_type_2": "S"}
        identified_info = {key: default_values[key] for key, s in point_structure.items()}

        # Identify the information in the point string
        for char in string:
            for key, value_dict in [('serve_type', Point.serve_type), ('player', Point.player), ('category', Point.cat), ('side', Point.side), ('shot_type', Point.shot), ('direction', Point.direction), ('player2', Point.player), ('side2', Point.side), ('shot_type_2', Point.shot)]:
                if char in value_dict and identified_info[key].startswith(default_values[key]):
                    identified_info[key] = char
                    break

        # If the point is a forced winner and player2 is not defined, set it to a player number that represents the other team
        if is_forced_winner and identified_info['player2'] == 'P':
            player1 = int(identified_info['player'])
            if player1 in [1, 2]:
                identified_info['player2'] = str(random.choice([3, 4]))
            else:
                identified_info['player2'] = str(random.choice([1, 2]))

        # Create the filled point string
        filled_string = ''.join([identified_info.get(key, '') for key in point_structure.keys()])

        # If the filled string is different from the original string, print both
        if filled_string != string:
            print(f"Original string: {string}")
            print(f"Filled string: {filled_string}")

        return filled_string

    def __init__(self, string: str) -> None:
        """
        Initialize a Point object from a string.

        Parameters
        ----------
        string : str
            A string containing information about the end of the point.
        """

        # Check if the string represents a serve marker
        if string.startswith("#"):
            print(f"Serve marker string: {string} \n")
            # Create a ServeMarker instance and change the class of the current instance
            serve_marker = ServeMarker(string)
            self.__class__ = ServeMarker
            self.__dict__.update(serve_marker.__dict__)
            # Print the string representation of the ServeMarker instance
            print(self)
            return
        
        point_min_length = max(s.stop for s in POINT_STRUCTURE.values())
        forced_winner_min_length = max(s.stop for s in FORCED_WINNER_POINT_STRUCTURE.values())


        # Check if the string is incomplete and, if so, complete it
        if len(string) != point_min_length and len(string) != forced_winner_min_length:
            print(f"Point string is incomplete: {string}, attempting to complete it... \n")
            string = self.complete_point_string(string)
            print(f"Completed point string: {string} \n")

        self._process_point_string(string)

        # Check if the point category is "f" and change the instance to Forced_winner
        if self.category == "f":
            forced_winner = Forced_winner(string)
            self.__class__ = Forced_winner
            self.__dict__.update(forced_winner.__dict__)


    def __str__(self) -> str:
        return f"Player {self.player} made a {self.category} on a {self.side} {self.shot_type} in the {self.direction}"

    @staticmethod
    def generate_valid_point_strings():
        # Filter out default values from each dictionary
        filtered_serve_type = {k: v for k, v in serve_type.items() if v != "Default Serve Type"}
        filtered_player = {k: v for k, v in player.items() if v != "Default Player"}
        filtered_cat = {k: v for k, v in cat.items() if v != "Default Category"}
        filtered_side = {k: v for k, v in side.items() if v != "Default Side"}
        filtered_shot = {k: v for k, v in shot.items() if v != "Default Shot"}
        filtered_direction = {k: v for k, v in direction.items() if v != "Default Direction"}

        # Create a dictionary mapping point structure keys to their corresponding filtered dictionaries
        key_to_dict = {
            "serve_type": filtered_serve_type,
            "player": filtered_player,
            "category": filtered_cat,
            "side": filtered_side,
            "shot_type": filtered_shot,
            "direction": filtered_direction,
        }

        # Generate all possible combinations of point structure values, excluding defaults
        valid_point_strings = []
        for keys in product(*[key_to_dict[key].keys() for key in POINT_STRUCTURE.keys() if key in key_to_dict]):
            point_string = "".join(keys)
            if point_string[POINT_STRUCTURE['category'].start] == "f":
                # Introduce a probability to limit the number of forced winners
                if random.random() < 0.5:
                    for player2 in range(1, 5):
                        if player2 != int(point_string[POINT_STRUCTURE['player'].start]):  # Ensure the second player is not the same as the first player
                            for side2_key in side.keys():
                                if side[side2_key] != "Default Side":  # Exclude default side
                                    for shot2_key in shot.keys():
                                        if shot[shot2_key] != "Default Shot":  # Exclude default shot
                                            valid_point_strings.append(point_string + str(player2) + side2_key + shot2_key)
            else:
                valid_point_strings.append(point_string)

        # Adjust the distribution of point strings in the final set
        forced_winner_strings = [point_string for point_string in valid_point_strings if point_string[POINT_STRUCTURE['category'].start] == "f"]
        unforced_error_strings = [point_string for point_string in valid_point_strings if point_string[POINT_STRUCTURE['category'].start] == "u"]
        winner_strings = [point_string for point_string in valid_point_strings if point_string[POINT_STRUCTURE['category'].start] == "w"]

        # Calculate the total number of valid point strings
        total_points = len(valid_point_strings)

        # Calculate the desired number of each type of point
        forced_winner_count = int(total_points * 0.4) # distribution based on existing db
        unforced_error_count = int(total_points * 0.3)
        winner_count = int(total_points * 0.3)

        # Take the desired number of each type of point
        forced_winner_strings = random.sample(forced_winner_strings, forced_winner_count)

        # Add duplicates of unforced errors and winners until the desired proportions are reached
        while len(unforced_error_strings) < unforced_error_count:
            unforced_error_strings += random.choices(unforced_error_strings, k=unforced_error_count - len(unforced_error_strings))

        while len(winner_strings) < winner_count:
            winner_strings += random.choices(winner_strings, k=winner_count - len(winner_strings))

        # Combine the lists to form the final set of valid point strings
        valid_point_strings = forced_winner_strings + unforced_error_strings + winner_strings

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
        if len(string) != len(FORCED_WINNER_POINT_STRUCTURE):
            raise ValueError(f"Invalid point string length for Forced Winner: {string}")
        self.player2 = int(string[FORCED_WINNER_POINT_STRUCTURE['player2']])
        self.side2 = Point.side[string[FORCED_WINNER_POINT_STRUCTURE['side2']]]
        self.shot_type_2 = Point.shot[string[FORCED_WINNER_POINT_STRUCTURE['shot_type_2']]]

class ServeMarker:
    def __init__(self, string: str) -> None:
        # Validate the string format
        if not string.startswith("#") or not string[1:].isdigit():
            raise ValueError(f"Invalid serve marker string: {string}")
        
        # Initialize the player attribute
        self.player = int(string[1:])

        print(self)
        
    def __str__(self) -> str:
        return f"Serve by Player {self.player}"

class InvalidPoint(Point):
    def __init__(self, string: str, error: Exception) -> None:
        # Set up logging
        logging.basicConfig(filename='invalid_points.log', level=logging.INFO)
        
        # Log the raw point and the error
        logging.info(f"Invalid point: {string}. Error: {error}")
        
        # Set the attributes to "none"
        self.player = "none"
        self.category = "none"
        self.side = "none"
        self.shot_type = "none"
        self.direction = "none"
        self.raw = string
