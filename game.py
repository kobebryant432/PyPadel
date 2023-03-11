class game():
    sc_tr = {0:'0', 1:'15',2:'30',3:'40',4:'Game'}
    def __init__(self) -> None:
        self.score_t1 = 0
        self.score_t2 = 0
        self.finished = False

    def __str__(self) -> str:
        if self.finished:
            return f'Team {self.winner} won the game - {game.sc_tr[self.score_t1]}-{game.sc_tr[self.score_t2]}'
        elif self.score_t1 == 3 and self.score_t2==3:
            return 'Golden Point!'
        else:
            return f'Game score is {game.sc_tr[self.score_t1]}-{game.sc_tr[self.score_t2]}'

    def update(self, team):
        if not self.finished:
            if team == 1:
                self.score_t1 +=1
            elif team == 2:
                self.score_t2 +=1
            else:
                print(f'Invalid team provided {team}')
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
        return f'{game.sc_tr[self.score_t1]}-{game.sc_tr[self.score_t2]}'
