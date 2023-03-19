class point():
    cat = {'f':'Forced Winner','u':'Unforced Error','w':'Winner'}
    side = {'fh':'Forehand','bh':'Backhand','hi':'High'}
    shot = {'v':'Volley','o':'Other','n':'Normal', 'g':'Glass','r':'return','l':'lob','s':'smash','V':'vibora','k':'kick','b':'bandeja', 'j':'bajada','k':'kick','f':'fake'}
    direction = {'c':'cross','p':'parallel','n':'net','l':'long', 'm':'middle'}

    def __init__(self, string) -> None:
        self.player = int(string[0])
        self.category = point.cat[string[1]]
        self.side = point.side[string[2:4]]
        #Dubbel use of letter v -> if high v = V = Vibora else it is a volley (v)
        if string[2:4] == 'hi':
            self.shot_type = self.shot['V']
        else:
            self.shot_type = self.shot[string[4]]
        self.direction = point.direction[string[5]]
        self.raw = string

    def __str__(self) -> str:
        return f'Player {self.player} made a {self.category} on a {self.side} {self.shot_type} in the {self.direction}'

class winner(point):
    def __init__(self, string) -> None:
        super().__init__(string)

class unforced_error(point):
    def __init__(self, string) -> None:
        super().__init__(string)

class forced_winner(point):
    def __init__(self, string) -> None:
        super().__init__(string)
        self.player2 = string[6]
        self.side2 = string[7:9]
        self.shot_type_2 = string[9]

