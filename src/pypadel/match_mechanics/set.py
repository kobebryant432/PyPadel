from .game import *


class Set:
    def __init__(self) -> None:
        self.score_t1 = 0
        self.score_t2 = 0
        self.current_game = Game()
        self.games = []
        self.serve_order = []
        self.finished = False

    def __str__(self):
        return f"set score: {self.score_t1}-{self.score_t2}"

    def update_server(self, player: int):
        order = {1: 2, 2: 1, 3: 4, 4: 3}
        if len(self.serve_order) < 4:
            self.serve_order.append(player)
            if len(self.serve_order) == 2:
                self.serve_order.append(order[self.serve_order[0]])
                self.serve_order.append(order[self.serve_order[1]])

    def update(self, point_winner, p):
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
                self.current_game = Game()
            print(self)
            self.is_fininshed()

    def is_fininshed(self):
        t1 = self.score_t1
        t2 = self.score_t2
        if (max(t1, t2) > 5 and max(t2, t1) - min(t2, t1) > 1) or (max(t1, t2) == 7):
            self.finished = True
            if t1 > t2:
                self.winner = 1
            if t2 > t1:
                self.winner = 2

    def score(self):
        return f"{self.score_t1}-{self.score_t2}"


class Tiebreak_set(Set):
    def __init__(self, target=10) -> None:
        super().__init__()
        self.target = target
        self.current_game = Tiebreak(target=target)

    def __str__(self):
        return f"Tie-break set score: {self.current_game.score_t1}-{self.current_game.score_t2} "

    def update(self, point_winner, p):
        self.current_game.update(point_winner, p)
        if self.current_game.finished:
            self.score_t1 = self.current_game.score_t1
            self.score_t2 = self.current_game.score_t2
            self.winner = self.current_game.winner
            self.finished = True
            print(self)

class Proset(Set):
    def __init__(self) -> None:
        super().__init__()

    def update(self, point_winner, p):
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
        t1 = self.score_t1
        t2 = self.score_t2
        if max(t1, t2) == 9:
            self.finished = True
            if t1 > t2:
                self.winner = 1
            if t2 > t1:
                self.winner = 2

    def score(self):
        return f"{self.score_t1}-{self.score_t2}"