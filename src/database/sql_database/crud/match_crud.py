import contextlib
import sqlite3
from pypadel import Match


class MatchCRUD:
    def __init__(self, db):
        self.db = db
        self.conn = db.conn

    def add_match(self, m, cat):  # Add a new argument for sheet name
        if not self.match_exists(m):
            # Include the sheet name in the values to insert
            values_to_insert = (
                m.date,
                m.tournament,
                m.r,
                m.players[0].name,
                m.players[1].name,
                m.sets_score,
                m.players[2].name,
                m.players[3].name,
                m.type,
                ",".join(m.raw_input),
                cat,
            )

            try:
                with contextlib.closing(self.conn.cursor()) as cursor, self.conn:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO matches (date, tournament, r, player_1, player_2, sets_score, player_3, player_4, match_type, raw_input, cat)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        values_to_insert,
                    )
                    # self.update_player_stats(m)
                    # Update player stats for each player involved in the match
                    for player in m.players:
                        self.db.player_manager.update_player_stats(player.name)
            except sqlite3.Error as e:
                print(f"An error occurred: {e.args[0]}")
        else:
            print("Match already exists, not inserting.")

    def get_match(self, pos):
        try:
            with contextlib.closing(self.conn.cursor()) as cursor, self.conn:
                cursor.execute("SELECT * FROM matches WHERE id=?", (pos,))
                match_record = cursor.fetchone()
                print(match_record)  # Print the record to debug
                if match_record:
                    return self._record_to_match_object(match_record)
                return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

    def get_matches(self, player_name):
        """
        Retrieves all matches a given player has participated in.
        """
        try:
            with contextlib.closing(self.conn.cursor()) as cursor, self.conn:
                cursor.execute(
                    """
                    SELECT * FROM matches WHERE player_1 = ? OR player_2 = ? OR player_3 = ? OR player_4 = ?
                """,
                    (player_name, player_name, player_name, player_name),
                )

                return cursor.fetchall()

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            return []

    def _record_to_match_object(self, record):
        return Match.from_record(record)

    def match_exists(self, m):
        values = (
            m.date,
            m.tournament,
            m.r,
            m.players[0].name,
            m.players[1].name,
            m.players[2].name,
            m.players[3].name,
            m.type,
            ",".join(m.raw_input),
        )
        with contextlib.closing(self.conn.cursor()) as cursor:
            cursor.execute(
                """
                SELECT 1 FROM matches WHERE date=? AND tournament=? AND r=? AND player_1=? AND player_2=? AND player_3=? AND player_4=? AND match_type=? AND raw_input=?
            """,
                values,
            )
            return cursor.fetchone() is not None