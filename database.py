import pandas as pd
from match import *
from player import player
import sys
import sys

class database():

    def __init__(self, name) -> None:
        self.name = name
        self.matches = None
        self.players = pd.DataFrame()

    def load_db(self, file, **kwargs):
        #Change log to file
        old_stdout = sys.stdout
        log_file = open("message.log","w")

        sys.stdout = log_file
        df = pd.read_excel(file, **kwargs)
        df.columns= df.columns.str.strip().str.lower()
        df['match'] = df.apply(lambda row: self.create_match(row), axis=1)
        self.matches = df

        #Reset log
        sys.stdout = old_stdout
        log_file.close()

    #ToDo -> Create a wat to add_match to a database of choice. 
    def add_match(self, m):
        self.matches.loc[len(self.matches)] = [m.date,m.tournament,m.r,m.players[0].name,m.players[1].name,m.players[2].name,m.players[3].name,m.type,','.join(m.raw_input),m]

    def export_all(self):
        for m in self.matches['match']:
            p1 = m.players[0].name.replace(' ','')
            p3 = m.players[3].name.replace(' ','')
            m.export(f'out/{m.tournament}_{p1}_{p3}.xlsx')

    #ToDo -> Make player list in database!
    def create_match(self, row):
        pl_name = [row.player_1,row.player_2,row.player_3,row.player_4]
        players = [player(name) for name in pl_name]
        m = match.create(int(row.match_type),players=players, date=row.date, tournament=row.tournament, r=str(row.r))
        data = [x.strip(' ') for x in row.data.split(",")]
        print(f'Starting to load: match {m}')
        m.play_match(data)
        return m
    
