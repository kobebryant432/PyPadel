from player import player
from match import match
import pandas as pd

def start_match():
    p1 = player(input('Name player 1: '))
    p2 = player(input('Name player 2: '))
    p3 = player(input('Name player 3: '))
    p4 = player(input('Name player 4: '))

    m = match([p1,p2,p3,p4])

    while True:
        x = input()
        if x=='Q':
            break
        print(len(x))
        if len(x) != 2:
            print(f'INCORRECT input. Expected one number and one letter, got {x}')
            x = input('Try again')
        if int(x[0])<1 or int(x[0])>4:
            print(f'INCORRECT input. There are only four players, player {int(x[0])} does not exist')
            x = input('Try again')
        m.update(x)
        print(m.stats)
    

start_match()


m = match([player(name) for name in ['p1','p2','p3','p4']])
m.play_match(['1F', '1U', '3F', '3F', '1F', '4U', '1F', '1F', '1F', '1F', '1F', '1F', '1F', '1F', '1F', '1F', '1F', '1F'])