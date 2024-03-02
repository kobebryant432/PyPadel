# point_mappings.py

POINT_STRUCTURE = {
    "serve_type": slice(0, 1),
    "player": slice(1, 2),
    "category": slice(2, 3),
    "side": slice(3, 5),
    "shot_type": slice(5, 6),
    "direction": slice(6, 7),
}

FORCED_WINNER_POINT_STRUCTURE = {
    **POINT_STRUCTURE,
    "player2": slice(7, 8),  # Indices updated
    "side2": slice(8, 10),
    "shot_type_2": slice(10, 11),
}

serve_type = {"e": "First Serve", "t": "Second Serve", "O": "Default Serve Type"}
player = {
    "1": "Player 1",
    "2": "Player 2",
    "3": "Player 3",
    "4": "Player 4",
}
cat = {"f": "Forced Winner", "u": "Unforced Error", "w": "Winner", "C": "Default Category"}
side = {"fh": "Forehand", "bh": "Backhand", "hi": "High", "hd": "High defense", "Si": "Default Side"}
shot = {
    "v": "Volley",
    "o": "Other",
    "n": "Normal",
    "g": "Glass",
    "r": "return",
    "l": "lob",
    "s": "smash",
    "V": "vibora",
    "k": "kick",
    "b": "bandeja",
    "j": "bajada",
    "f": "fake",
    "z": "double fault",
    "S": "Default Shot",
}
direction = {
    "c": "cross",
    "p": "parallel",
    "n": "net",
    "l": "long",
    "m": "middle",
    "d": "dropshot",
    "k": "dunk",
    "g": "globo",
    "f": "fence",
    "D": "Default Direction",
}