class point():
    #Do translation to human tekst
    def __init__(self, string) -> None:
        self.player = int(string[0])
        self.category = string[1]
        self.side = string[2:4]
        self.shot_type = string[4]
        self.direction = string[5]
        self.raw = string

    def __str__(self) -> str:
        return f'Player {self.player} made a {self.category} on the {self.side} side playing a {self.shot_type} {self.direction}'
    
class forced_winner(point):
    def __init__(self, string) -> None:
        super().__init__(string)
        self.player2 = string[6]
        self.side2 = string[7:9]
        self.shot_type_2 = string[9]

