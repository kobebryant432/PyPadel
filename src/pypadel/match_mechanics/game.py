class Game:
    """
    Class to represent a game.

    Attributes
    ----------
    sc_tr : dict
        A dictionary to translate number of points to tennis scores.

    score_t1 : int
        The number of points won by team 1.
    score_t2 : int
        The number of points won by team 2.
    points : dict
        A dictionary containing the game score as keys and the corresponding points as values.
    finished : bool
        Indicates whether the game has finished or not.
    winner : int
        The team number (1 or 2) that won the game if the game is finished.
    """
    sc_tr = {0: "0", 1: "15", 2: "30", 3: "40", 4: "Game"}

    def __init__(self) -> None:
        """Initialize a Game object."""
        self.score_t1 = 0
        self.score_t2 = 0
        self.points = {}
        self.finished = False

    def __str__(self) -> str:
        """Generate a string representation of the current state of the Game object."""
        if self.finished:
            return f"Team {self.winner} won the game - {self.score}"
        elif self.score_t1 == 3 and self.score_t2 == 3:
            return "Golden Point!"
        else:
            return (
                f"Game score is {self.score}"
            )

    def update(self, team, point):
        """Update the game with a new point.

        After updating the game with the point a check is done to see if the game has finished.

        Parameters
        ----------
        team : int
            The team number (1 or 2) that scored the point.
        point : Point
            The Point object representing the scored point.

        Notes
        -----
        - The `points` dictionary is updated with the newly scored point.
        - The game scores for the respective teams (`score_t1` and `score_t2`) are updated.
        - The `is_finished` method is called to check if the game has finished.
        - The method also prints the current game state to the console.
        """
        self.points[self.score] = point
        if not self.finished:
            if team == 1:
                self.score_t1 += 1
            elif team == 2:
                self.score_t2 += 1
            else:
                print(f"Invalid team provided {team}")
            self.is_finished()
            print(self)
        else:
            print(self)

    def is_finished(self):
        """Check if the game has finished and determine who won the game.

        A standard game uses golden point and is finished when a team makes 4 points. The status of the game is 
        updated to finished and a winner is assigned if the game is finished.
        """
        if self.score_t1 == 4:
            self.winner = 1
            self.finished = True
        if self.score_t2 == 4:
            self.winner = 2
            self.finished = True

    @property
    def score(self):
        """Get the current game score in the format "score_team1-score_team2".

        Returns
        -------
        str
            The game score.
        """

        return f"{Game.sc_tr[self.score_t1]}-{Game.sc_tr[self.score_t2]}"

    def game_summary(self):
        """Print a summary of all the points in the game."""
        for score, point in self.points.items():
            print(f"Score {score} - {point}")


class Tiebreak(Game):
    """
    Class to represent a tie-break game, a specialized form of a game.

    Parameters
    ----------
    target : int, optional
        The target score to win the tie-break, default is 7.

    Attributes
    ----------
    target : int
        The target score to win the tie-break.
    score_t1 : int
        The score of team 1.
    score_t2 : int
        The score of team 2.
    points : dict
        A dictionary to store points along with their corresponding scores.
    finished : bool
        Flag indicating if the tie-break game is finished.
    winner : int
        The team number (1 or 2) that won the tie-break game.

    Inherits
    --------
    Game : class
        The base class for representing games.
    """
    def __init__(self, target=7) -> None:
        super().__init__()
        self.target = target

    def __str__(self) -> str:
        """Generate a string representation of the current state of the Tiebreak object."""
        if self.finished:
            return f"Team {self.winner} won the tie-break - {self.score_t1}-{self.score_t2}"
        else:
            return f"Tie-break score is {self.score_t1}-{self.score_t2}"

    def is_finished(self):
        """Check if the game has finished and determine who won the tie-break.

        A tie-break is finished when a team reaches the target amount of points with a 2 point gap. 
        The status of the tie-break is updated to finished and a winner is assigned if the tie-break is finished.
        """
        if self.score_t1 >= self.target and self.score_t1 - self.score_t2 > 1:
            self.winner = 1
            self.finished = True
        if self.score_t2 >= self.target and self.score_t2 - self.score_t1 > 1:
            self.winner = 2
            self.finished = True

    @property
    def score(self):
        """Get the current game score in the format "score_team1-score_team2".

        Returns
        -------
        str
            The game score.
        """
        return f"{self.score_t1}-{self.score_t2}"
    
class Adv_game(Game):
    """
    Class to represent a game with advantage, a specialized form of a game.

    Attributes
    ----------
    score_t1 : int
        The score of team 1.
    score_t2 : int
        The score of team 2.
    points : dict
        A dictionary to store points along with their corresponding scores.
    finished : bool
        Flag indicating if the tie-break game is finished.
    winner : int
        The team number (1 or 2) that won the tie-break game.

    Inherits
    --------
    Game : class
        The base class for representing games.
    """
    def __init__(self) -> None:
        super().__init__()

    def is_finished(self):
        """Check if the game has finished and determine who won the game.

        An advantage game is finished when a team makes at least 4 points and has a 2 point lead over the other team. 
        The status of the game is updated to finished and a winner is assigned if the game is finished.
        """
        if self.score_t1 >= 4 and self.score_t1 - self.score_t2 > 1:
            self.winner = 1
            self.finished = True
        if self.score_t2 >= 4 and self.score_t2 - self.score_t1 > 1:
            self.winner = 2
            self.finished = True

    def __str__(self) -> str:
        if self.finished:
            return f"Team {self.winner} won the game - {self.score}"
        else:
            return (
                f"Game score is {self.score}"
            )

    @property
    def score(self):
        """Get the current game score in the format "score_team1-score_team2".

        Returns
        -------
        str
            The game score.
        """
        if self.score_t1 < 4 and self.score_t2 < 4:
            return f"{Game.sc_tr[self.score_t1]}-{Game.sc_tr[self.score_t2]}"
        elif self.score_t1 - self.score_t2 ==1:
            return "Adv-40"
        elif self.score_t2 - self.score_t1 ==1:
            return "40-Adv"
        elif self.score_t1 > self.score_t2:
            return "Game-40"
        elif self.score_t2 > self.score_t1:
            return "40-Game"
        else:
            return "40-40"