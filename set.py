from game import game

class set():
    def __init__(self) -> None:
        self.score_t1 = 0
        self.score_t2 = 0
        self.current_game = game()
        self.games = []
        self.finished = False

    def __str__(self):
        return f'Set score: {self.score_t1}-{self.score_t2} '

    def update(self, point_winner):
        self.current_game.update(point_winner)
        if self.current_game.finished:
            winner = self.current_game.winner
            if winner == 1:
                self.score_t1 += 1
            else: 
                self.score_t2 += 1
            self.games.append(self.current_game)
            self.current_game = game()
            print(self)
            self.is_fininshed()
    
    def is_fininshed(self):
        t1 = self.score_t1
        t2 = self.score_t2
        if ((max(t1, t2) > 5 & t2-t1>1) or (max(t1, t2) == 7)):
            self.finished = True
            if t1 > t2:
                self.winner = 1
            if t2 > t1:
                self.winner = 2
    
    def score(self):
        return f'{self.score_t1}-{self.score_t2}'