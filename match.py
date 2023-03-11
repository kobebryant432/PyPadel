import pandas as pd
from set import set

class match:
    cols = ['Forced Error', 'Unforced Error']
    input_map = {'F':'Forced Error', 'U':'Unforced Error'}
    team = {1:0, 2:0, 3:1, 4:1}
    team_map = {'F':1,'U':1}
    
    def __init__(self, players) -> None:
        self.players = players
        self.stats = pd.DataFrame(0, columns=match.cols,index=[p.name for p in players])
        self.raw_score = []
        self.current_set = set()
        self.sets = []
        self.finished = False

    def update(self, x):
        self.stats.at[self.players[int(x[0])-1].name, match.input_map[x[1]]] += 1
        team_action = match.team[int(x[0])]
        point_winner = (team_action+match.team_map[x[1]])%2
        self.current_set.update(point_winner+1)
        if self.current_set.finished:
            self.sets.append(self.current_set)
            self.currentset = set()
            for i,x in enumerate(self.sets):
                print(i, x)
        self.raw_score.append((len(self.sets)+1,self.current_set.score(),len(self.current_set.games)+1,self.current_set.current_game.score(),x))

    def play_match(self, list):
        for l in list:
            self.update(l)
    
    
