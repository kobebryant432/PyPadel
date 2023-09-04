import sqlite3
from pypadel import Match
from .point_stats import PointStatistics


class PlayerStats:
    def __init__(self, db):
        self.db = db
        self.conn = db.conn
        self.point_stats = PointStatistics(self.conn)

    def update_total_matches(self, player_name):
        # Check the return value of get_matches
        matches = self.db.match_manager.get_matches(player_name)
        total_matches = len(matches)

        if total_matches == 0:
            print(
                f"Warning: No matches found for {player_name}. This might be unexpected."
            )

        try:
            with self.conn:
                updated_rows = self.conn.execute(
                    """
                    UPDATE players SET nr_matches = ? WHERE player_name = ?
                """,
                    (total_matches, player_name),
                ).rowcount

                # Check if the player's name exists in the database
                if updated_rows == 0:
                    print(
                        f"Warning: No rows updated for {player_name}. Player might not exist in the database."
                    )

        except sqlite3.Error as e:
            print(f"An error occurred during updating total matches: {e}")

    def update_win_rate(self, player_name):
        # Calculate the win rate using the logic provided
        calculated_win_rate = self.win_rate(player_name)

        try:
            with self.conn:
                updated_rows = self.conn.execute(
                    """
                    UPDATE players SET win_rate = ? WHERE player_name = ?
                """,
                    (calculated_win_rate, player_name),
                ).rowcount

                # Check if the player's name exists in the database
                if updated_rows == 0:
                    print(
                        f"Warning: No rows updated for {player_name} in update_win_rate method. Player might not exist in the database."
                    )
        except sqlite3.Error as e:
            print(f"An error occurred during updating win rate: {e}")

    def update_avg_stats(self, player_name):
        # Calculate the average stats per game using the existing function
        stats = self.get_avg_per_game_stats(player_name)

        avg_unforced_errors = stats["avg_unforced_errors_per_game"]
        avg_winners = stats["avg_winners_per_game"]

        try:
            with self.conn:
                # Update unforced errors
                updated_rows_unforced_errors = self.conn.execute(
                    """
                    UPDATE players SET avg_unf_error_game = ? WHERE player_name = ?
                    """,
                    (f"{avg_unforced_errors:.2f}", player_name),
                ).rowcount

                # Update winners
                updated_rows_winners = self.conn.execute(
                    """
                    UPDATE players SET avg_winners_game = ? WHERE player_name = ?
                    """,
                    (f"{avg_winners:.2f}", player_name),
                ).rowcount

                # Check if the player's name exists in the database
                if updated_rows_unforced_errors == 0:
                    print(
                        f"Warning: No rows updated for {player_name} in update_avg_unforced_errors. Player might not exist in the database."
                    )

                if updated_rows_winners == 0:
                    print(
                        f"Warning: No rows updated for {player_name} in update_avg_winners. Player might not exist in the database."
                    )

        except sqlite3.Error as e:
            print(f"An error occurred during updating statistics: {e}")

    def retrieve_point_statistics(self, player_name, match_id=None, recent_n=None):
        return self.point_stats.get_point_statistics(player_name, match_id, recent_n)

    def win_rate(self, player_name):
        matches = self.db.match_manager.get_matches(player_name)
        wins = 0

        for match in matches:
            sets = match["sets_score"].split(
                ","
            )  # First split by commas to get the sets

            player1_2_sets_won = 0
            player3_4_sets_won = 0

            for set_score in sets:
                # Check if set_score has the hyphen
                if "-" not in set_score:
                    print(f"Invalid set score format: {set_score}")
                    continue

                # Split and try converting to integers
                parts = set_score.split("-")
                try:
                    player1_2_score, player3_4_score = map(int, parts)
                except ValueError:
                    print(f"Invalid score values in set score: {set_score}")
                    continue

                if player1_2_score > player3_4_score:
                    player1_2_sets_won += 1
                else:
                    player3_4_sets_won += 1

            if player_name == match["player_1"] or player_name == match["player_2"]:
                if player1_2_sets_won > player3_4_sets_won:
                    wins += 1
            elif player_name == match["player_3"] or player_name == match["player_4"]:
                if player3_4_sets_won > player1_2_sets_won:
                    wins += 1

        win_rate = f"{wins / len(matches) * 100 if matches else 0:.0f}%"

        return win_rate

    def get_avg_per_game_stats(self, player_name: str, match_id=None):
        """
        Retrieves the average statistics over all the matches a given player has participated in.
        Optionally, for a specific match if match_id is provided.
        Returns a dictionary containing average statistics per game (like unforced errors, winners, etc.).
        """
        if match_id:
            # Get specific match data for the player
            matches_data = [self.db.match_manager.get_match(match_id)]
        else:
            # Get all matches for the player
            matches_data = self.db.match_manager.get_matches(player_name)

        # Initialize total counters
        total_unforced_errors = 0
        total_winners = 0
        total_points_lost = 0
        total_games_played = 0

        for match_data in matches_data:
            # Convert the raw data into a Match instance
            match_instance = Match.from_record(match_data)

            # Get point statistics for the player for this match
            stats = self.retrieve_point_statistics(
                player_name, match_id=match_data["id"]
            )

            total_unforced_errors += stats["unforced_errors"]
            total_winners += stats["winners"]
            total_winners += stats["forced_winners"]
            total_points_lost += stats["total_points_lost"]
            total_games_played += match_instance.total_games_played()

            print(
                f"Match ID: {match_data['id']}, Unforced errors in this match: {stats['unforced_errors']}, Winners in this match: {stats['winners']}, Games played in this match: {match_instance.total_games_played()}"
            )

        # Calculate average unforced errors and winners per game
        if total_points_lost != 0 and total_games_played != 0:
            avg_unforced_errors_per_game = total_unforced_errors / total_games_played
            avg_winners_per_game = total_winners / total_games_played
        else:
            avg_unforced_errors_per_game = 0
            avg_winners_per_game = 0

        return {
            "avg_unforced_errors_per_game": avg_unforced_errors_per_game,
            "avg_winners_per_game": avg_winners_per_game,
        }
