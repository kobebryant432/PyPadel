import pandas as pd
from set import set
from points import *

class match:
    input_map = {'f':'Forced Error', 'u':'Unforced Error', 'w':'Winner'}
    #Sub Categories -> 
    team = {1:0, 2:0, 3:1, 4:1}
    team_map = {'w':0,'f':0,'u':1}
    
    def __init__(self, players) -> None:
        self.players = players
        self.raw_score = []
        self.current_set = set()
        self.sets = []
        self.finished = False

    def update(self, x):
        if x[1] == 'f':
            p = forced_winner(x)
        else:
            p = point(x)
        self.raw_score.append(
            (len(self.sets)+1,self.current_set.score(),
             len(self.current_set.games)+1,
             self.current_set.current_game.score(),
             self.players[p.player-1].name,
             match.team[p.player],
             p.category,
             p.side,
             p.shot_type,
             p.direction,
             p))
        team_action = match.team[int(x[0])]
        point_winner = (team_action+match.team_map[x[1]])%2
        self.current_set.update(point_winner+1, p)
        if self.current_set.finished:
            self.sets.append(self.current_set)
            self.current_set = set()
            for i,se in enumerate(self.sets):
                print(i, se)


    def play_match(self, list):
        for l in list:
            self.update(l)

    def get_summary(self):
        def color(val):
            if val > 2:
                color = 'red'
            elif val > 1:
                color = 'orange'
            else:
                color = None
            return 'background-color: %s' % color
        def color_good(val):
            if val > 2:
                color = 'green'
            elif val > 1:
                color = 'blue'
            else:
                color = None
            return 'background-color: %s' % color
        df = pd.DataFrame(self.raw_score, columns=['set','set_score','game','game_score','player','team','category','side','shot_type','direction','raw'])
        p = pd.pivot_table(df, values='raw',index=['category','team','player'],columns=['set','set_score'], aggfunc='count').fillna(0).astype(int)
        idx = pd.IndexSlice[p.index.get_level_values(level=0)=='u', :]
        idxg = pd.IndexSlice[p.index.get_level_values(level=0).isin(['w','f']), :]
        p = p.style.applymap(color, subset=idx).applymap(color_good, subset=idxg)
        return p

    def game_summary(self, set, game):
        print(f'Set {set} , Game {game}')
        self.sets[set-1].games[game-1].game_summary()
    
    