import sqlite3
from database.sql_database.stats import PlayerStats


class PlayerCRUD:
    def __init__(self, db):
        self.db = db
        self.conn = db.conn
        self.stats = PlayerStats(db)  # Instantiate the PlayerStats subclass

    def add_player(self, player_name, side, cat):
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT OR IGNORE INTO players (player_name, side, cat)
                    VALUES (?, ?, ?)
                """,
                    (player_name, side, cat),
                )
                print(f"Player {player_name} added to the database.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

    def update_player_stats(self, player_name):
        self.stats.update_total_matches(player_name)
        self.stats.update_win_rate(player_name)
        self.stats.update_avg_stats(player_name)
