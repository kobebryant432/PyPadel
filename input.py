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
        if input_ok(x):
            m.update(x)
    
def input_ok(x):
    return True

#start_match()
    

m = match([player(name) for name in ['Ilse','Fien','Kelly Maene','Elizabeth Lamaire']])
m.play_match(['1ubhnn', '1ufhsn', '2whivc', '2wbhvc', '3ffhvc1fhn', '4ubhsn', '4wfhom', '1wbhgc', '3ufhvn', '2ubhgn', '3fhibc2fhn', '3fhisp1fhn', '2ufhgl', '4ubhvn', '4ufhnp', '2ufhvn', '4wbhnc', '1ubhvp', '4ubhrl', '4fhisp1fhn', '3wfhvp', '4uhivp', '3uhivc', '4uhisn', '4ffhvp1fhn', '2ufhlp', '1wfhvm', '4ufhnn', '2ubhnn', '4ubhgn', '4wfhvp', '2wfhvp', '1ufhsl', '3whisp', '4wfhgc', '4ufhvl', '1ufhrn', '2ubhnn', '3whisc', '3ubhnn', '4ufhgn', '3ubhrl', '1ufhgn', '3ufhrl', '2ubhnn', '2ufhvl', '1ufhnc', '4wbhvc', '4ufhgn', '2whivp', '4wfhnc', '2uhisl', '4ufhvp', '1uhivc', '4ubhrl', '3ubhvn', '4ufhvp', '2wbhnc', '4whivc', '4uhivn', '1wfhvm', '1wfhvm', '4fhijm2fhv', '2ufhvn', '2wfhvp', '1whivm', '1ufhnn', '4ufhvn', '4wfhvp', '1fbhvp4bhv', '1ufhnn', '4wfhvc', '2ufhgn', '2whivp', '4ufhvp', '3wfhvc', '3uhivc', '2ubhvl', '4fbhnc2bhn', '3wbhvp', '2ubhrn', '4wfhvp', '2ubhrn', '3ufhrn', '1ufhnn', '4wbhnm', '3wbhvc', '3ufhrn', '2whivp', '4wfhgc', '2ubhnp', '1ubhnv', '3ubhnn', '2ubhrl', '1ufhrn', '3wfhnm', '2ubhll', '3ubhvl', '2ufhvp', '1ufhvl'])
df = m.get_summary()
m.game_summary(1,7)
df1 = m.get_det_summary()
df2 = m.get_det_summary(dir=True)