from match_mechanics.game import Adv_game, Game, Tiebreak


class Set:
    """Class to represent a set in a sports match.

    Attributes
    ----------
    score_t1 : int
        The set score of team 1.
    score_t2 : int
        The set score of team 2.
    current_game : Game
        The current game being played within the set.
    adv_game : bool
        Flag indicating whether the set uses advantage games.
    games : list
        A list to store the games played in the set.
    serve_order : list
        A list to track the players serving order in each set.
    finished : bool
        Flag indicating if the set is finished.
    winner : int
        The team number (1 or 2) that won the set if the set is finished.
    """
    def __init__(self, adv_game=False) -> None:
        """
        Initialize a new set.

        Parameters
        ----------
        adv_game : bool, optional
            Flag indicating whether the set uses advantage games, by default False.

        Attributes
        ----------
        score_t1 : int
            The set score of team 1.
        score_t2 : int
            The set score of team 2.
        current_game : Game
            The current game being played within the set.
        adv_game : bool
            Flag indicating whether the set uses advantage games.
        games : list
            A list to store the games played in the set.
        serve_order : list
            A list to track the players serving order in each set.
        finished : bool
            Flag indicating if the set is finished.
        winner : int
            The team number (1 or 2) that won the set if the set is finished.
        """
        self.score_t1 = 0
        self.score_t2 = 0
        if adv_game:
            self.current_game = Adv_game()
        else:
            self.current_game = Game()
        self.adv_game = adv_game
        self.games = []
        self.serve_order = []
        self.finished = False

    def __str__(self):
        """Get a string representation of the set."""
        return f"set score: {self.score_t1}-{self.score_t2}"

    def update_server(self, player: int):
        """Update the serving order.

        After updating the servers with 2 players (one from each team) the server order is uniquely defined for the set.
        Adding more servers will have no impact.
        
        Parameters
        ----------
        player : int
            The player number (1 or 2) serving that game.
        """
        order = {1: 2, 2: 1, 3: 4, 4: 3}
        if len(self.serve_order) < 4:
            self.serve_order.append(player)
            if len(self.serve_order) == 2:
                self.serve_order.append(order[self.serve_order[0]])
                self.serve_order.append(order[self.serve_order[1]])

    def update(self, point_winner, p):
        """Update the set with a new point.

        If the point finishes the current game the set score is updated, a check is performed to see if the set is finished, 
        a new game or tie-break is started. A tie-break is started at 6-6.

        Parameters
        ----------
        point_winner : int
            The team number (1 or 2) that won the point.
        p : Point
            The point scored.
        """
        self.current_game.update(point_winner, p)
        if self.current_game.finished:
            winner = self.current_game.winner
            if winner == 1:
                self.score_t1 += 1
            else:
                self.score_t2 += 1
            self.games.append(self.current_game)
            if self.score_t1 == 6 and self.score_t2 == 6:
                self.current_game = Tiebreak()
            else:
                if self.adv_game:
                    self.current_game = Adv_game()
                else:
                    self.current_game = Game()
            print(self)
            self.is_fininshed()

    def is_fininshed(self):
        """Check if the set is finished and determine the winner.

        A standard set is finished if one team reaches 6 with a two game gap or a team reaches 7 games (wins a tie-break).
        """
        t1 = self.score_t1
        t2 = self.score_t2
        if (max(t1, t2) > 5 and max(t2, t1) - min(t2, t1) > 1) or (max(t1, t2) == 7):
            self.finished = True
            if t1 > t2:
                self.winner = 1
            if t2 > t1:
                self.winner = 2

    def score(self):
        """Get the current set score in the format "score_team1-score_team2".

        Returns
        -------
        str
            The game score.
        """
        return f"{self.score_t1}-{self.score_t2}"


class Tiebreak_set(Set):
    """
    Class to represent a tie-break set, inheriting from the Set class.

    Attributes
    ----------
    target : int
        The target score for the tie-break set.
    score_t1 : int
        The set score of team 1.
    score_t2 : int
        The set score of team 2.
    current_game : Game
        The current game being played within the set.
    adv_game : bool
        Flag indicating whether the set uses advantage games.
    games : list
        A list to store the games played in the set.
    serve_order : list
        A list to track the players serving order in each set.
    finished : bool
        Flag indicating if the set is finished.
    winner : int
        The team number (1 or 2) that won the set if the set is finished.

    Inherits
    --------
    Set : class
        The base class for representing sets.
    """
    def __init__(self, target=10) -> None:
        """Initialize a new tie-break set.

        Parameters
        ----------
        target : int, optional
            The target score for the tie-break set, by default 10.

        Attributes
        ----------
        target : int
            The target score for the tie-break set.
        current_game : Tiebreak
            The current game being played within the tie-break set.
        """
        super().__init__()
        self.target = target
        self.current_game = Tiebreak(target=target)

    def __str__(self):
        return f"Tie-break set score: {self.current_game.score_t1}-{self.current_game.score_t2} "

    def update(self, point_winner, p):
        """Update the set with a new point.

        As a tie-break set contains only one game (namely the tie-break) it is finished once the game is finished.

        Parameters
        ----------
        point_winner : int
            The team number (1 or 2) that won the point.
        p : Point
            The point scored.
        """
        self.current_game.update(point_winner, p)
        if self.current_game.finished:
            self.score_t1 = self.current_game.score_t1
            self.score_t2 = self.current_game.score_t2
            self.winner = self.current_game.winner
            self.finished = True
            print(self)

class Proset(Set):
    """Class to represent a pro-set a set to 9 games, inheriting from the Set class.

    Attributes
    ----------

    score_t1 : int
        The set score of team 1.
    score_t2 : int
        The set score of team 2.
    current_game : Game
        The current game being played within the set.
    adv_game : bool
        Flag indicating whether the set uses advantage games.
    games : list
        A list to store the games played in the set.
    serve_order : list
        A list to track the players serving order in each set.
    finished : bool
        Flag indicating if the set is finished.
    winner : int
        The team number (1 or 2) that won the set if the set is finished.

    Inherits
    --------
    Set : class
        The base class for representing sets.
    """
    def __init__(self, adv_game=True) -> None:
        """
        Initialize a new pro-set.

        Parameters
        ----------
        adv_game : bool, optional
            Flag indicating whether the set uses advantage games, by default True.

        Attributes
        ----------
        score_t1 : int
            The set score of team 1.
        score_t2 : int
            The set score of team 2.
        current_game : Game
            The current game being played within the set.
        adv_game : bool
            Flag indicating whether the set uses advantage games.
        games : list
            A list to store the games played in the set.
        serve_order : list
            A list to track the players serving order in each set.
        finished : bool
            Flag indicating if the set is finished.
        winner : int
            The team number (1 or 2) that won the set if the set is finished.
        """
        super().__init__(adv_game=adv_game)

    def update(self, point_winner, p):
        """Update the set with a new point.

        If the point finishes the current game the set score is updated, a check is performed to see if the pro-set is finished, 
        a new game or tie-break is started. A tie-break is started at 8-8.

        Parameters
        ----------
        point_winner : int
            The team number (1 or 2) that won the point.
        p : Point
            The point scored.
        """
        self.current_game.update(point_winner, p)
        if self.current_game.finished:
            winner = self.current_game.winner
            if winner == 1:
                self.score_t1 += 1
            else:
                self.score_t2 += 1
            self.games.append(self.current_game)
            if self.score_t1 == 8 and self.score_t2 == 8:
                self.current_game = Tiebreak()
            else:
                self.current_game = Game()
            print(self)
            self.is_fininshed()

    def is_fininshed(self):
        """Check if the set is finished and determine the winner.

        A pro-set is finished if one team reaches 9 games.
        """
        t1 = self.score_t1
        t2 = self.score_t2
        if max(t1, t2) == 9:
            self.finished = True
            if t1 > t2:
                self.winner = 1
            if t2 > t1:
                self.winner = 2

    def score(self):
        """Get the current set score in the format "score_team1-score_team2".

        Returns
        -------
        str
            The game score.
        """
        return f"{self.score_t1}-{self.score_t2}"