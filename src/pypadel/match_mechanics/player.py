class Player:
    """Class to represent a player.

    Parameters
    ----------
    name : str
        The name of the player.

    Attributes
    ----------
    name : str
        The name of the player.
    matches : list
        A list containing Match objects representing the player's matches.
    """
    def __init__(self, name:str) -> None:
        """
        Initialize a Player object.

        Parameters
        ----------
        name : str
            The name of the player.
        """
        self.name = name
        self.matches = []

    def add_match(self, m):
        """
        Add a match to the player's list of matches.

        Parameters
        ----------
        m : Match
            The match to be added.
        """
        self.matches.append(m)
