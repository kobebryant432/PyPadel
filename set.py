from game import game
from tie_break import tie_break

class set():
    def __init__(self) -> None:
        self.score_t1 = 0
        self.score_t2 = 0
        self.current_game = game()
        self.games = []
        self.finished = False

    def __str__(self):
        return f'Set score: {self.score_t1}-{self.score_t2} '

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
                self.current_game = tie_break()
            else:
                self.current_game = game()
            print(self)
            self.is_fininshed()
    
    def is_fininshed(self):
        t1 = self.score_t1
        t2 = self.score_t2
        if ((max(t1, t2) > 5 and t2-t1>1) or (max(t1, t2) == 7)):
            self.finished = True
            if t1 > t2:
                self.winner = 1
            if t2 > t1:
                self.winner = 2
    
    def score(self):
        return f'{self.score_t1}-{self.score_t2}'