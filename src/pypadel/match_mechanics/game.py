class Game:
    sc_tr = {0: "0", 1: "15", 2: "30", 3: "40", 4: "Game"}

    def __init__(self) -> None:
        self.score_t1 = 0
        self.score_t2 = 0
        self.points = {}
        self.finished = False

    def __str__(self) -> str:
        if self.finished:
            return f"Team {self.winner} won the game - {Game.sc_tr[self.score_t1]}-{Game.sc_tr[self.score_t2]}"
        elif self.score_t1 == 3 and self.score_t2 == 3:
            return "Golden Point!"
        else:
            return (
                f"Game score is {Game.sc_tr[self.score_t1]}-{Game.sc_tr[self.score_t2]}"
            )

    def update(self, team, point):
        self.points[self.score()] = point
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
        if self.score_t1 == 4:
            self.winner = 1
            self.finished = True
        if self.score_t2 == 4:
            self.winner = 2
            self.finished = True

    def score(self):
        return f"{Game.sc_tr[self.score_t1]}-{Game.sc_tr[self.score_t2]}"

    def game_summary(self):
        for score, point in self.points.items():
            print(f"Score {score} - {point}")


class Tiebreak(Game):
    def __init__(self, target=7) -> None:
        super().__init__()
        self.target = target

    def __str__(self) -> str:
        if self.finished:
            return f"Team {self.winner} won the tie-break - {self.score_t1}-{self.score_t2}"
        else:
            return f"Tie-break score is {self.score_t1}-{self.score_t2}"

    def is_finished(self):
        if self.score_t1 >= self.target and self.score_t1 - self.score_t2 > 1:
            self.winner = 1
            self.finished = True
        if self.score_t2 >= self.target and self.score_t2 - self.score_t1 > 1:
            self.winner = 2
            self.finished = True

    def score(self):
        return f"{self.score_t1}-{self.score_t2}"
