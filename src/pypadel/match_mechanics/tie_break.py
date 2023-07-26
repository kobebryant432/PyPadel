class Tie_break:
    def __init__(self, points=7) -> None:
        self.points = points
        self.score_t1 = 0
        self.score_t2 = 0
        self.finished = False

    def __str__(self) -> str:
        if self.finished:
            return f"Team {self.winner} won the tie-break - {self.score_t1}-{self.score_t2}"
        else:
            return f"Game score is {self.score_t1}-{self.score_t2}"

    def update(self, team):
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
        if self.score_t1 >= self.points and self.score_t1 - self.score_t2 > 1:
            self.winner = 1
            self.finished = True
        if self.score_t1 >= self.points and self.score_t2 - self.score_t1 > 1:
            self.winner = 2
            self.finished = True

    def score(self):
        return f"{self.score_t1}-{self.score_t2}"
