MATCHES_TABLE = """
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY,
    date TEXT,
    tournament TEXT,
    r TEXT,
    player_1 TEXT,
    player_2 TEXT,
    sets_score TEXT,
    player_3 TEXT,
    player_4 TEXT,
    match_type INTEGER,
    raw_input TEXT,
    cat TEXT,  -- New column for sheet name
    adv_game INTEGER,  -- New column for adv_game
    UNIQUE(date, tournament, r, player_1, player_2, player_3, player_4, match_type, raw_input)
)
"""

PLAYERS_TABLE = """
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT UNIQUE,
    side TEXT,
    cat TEXT,
    nr_matches INTEGER DEFAULT 0,
    win_rate REAL DEFAULT 0.0,
    avg_unf_error_game REAL DEFAULT 0.0,
    avg_winners_game REAL DEFAULT 0.0,
    UNIQUE(player_name)
)
"""
