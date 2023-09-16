# point_mappings.py

POINT_STRUCTURE = {
    "player": slice(0, 1),
    "category": slice(1, 2),
    "side": slice(2, 4),
    "shot_type": slice(4, 5),
    "direction": slice(5, 6),
}

FORCED_WINNER_POINT_STRUCTURE = {
    **POINT_STRUCTURE,
    "player2": slice(6, 7),
    "side2": slice(7, 9),
    "shot_type_2": slice(9, 10),
}

cat = {"f": "Forced Winner", "u": "Unforced Error", "w": "Winner"}
side = {"fh": "Forehand", "bh": "Backhand", "hi": "High", "hd": "High defense"}
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
}