import pandas as pd
from match import match
from player import player

class database():
    def __init__(self, name) -> None:
        self.name = name
        self.matches = None

    def load_db(self, file, **kwargs):
        df = pd.read_excel(file, **kwargs)
        df.columns= df.columns.str.strip().str.lower()
        df['match'] = df.apply(lambda row: create_match(row), axis=1)
        self.matches = df


def create_match(row):
    players = [player(name) for name in [row.player_1,row.player_2,row.player_3,row.player_4]]
    m = match(players=players, date=row.date, tournament=row.tournament, round=row.round)
    data = [x.strip(' ') for x in row.data.split(",")]
    print(f'Starting to load: match {m}')
    m.play_match(data)
    return m