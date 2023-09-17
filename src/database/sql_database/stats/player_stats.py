import sqlite3
import logging
from pypadel import Match, Set, Game, Point
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

    def get_serve_percentages(self, player_name, match_id=None, enable_logging=False):
        """
        This method calculates the first and second serve percentages for a given player.
        Optionally, it can calculate the serve percentages for a specific match if a match_id is provided.
        It also has an option to enable or disable logging.

        Args:
            player_name (str): The name of the player.
            match_id (int, optional): The ID of a specific match. Defaults to None.
            enable_logging (bool, optional): Whether to enable logging. Defaults to False.

        Returns:
            tuple: The first and second serve percentages.
        """

        # Create a logger
        logger = logging.getLogger(__name__)
        # Set the logging level based on the enable_logging parameter
        logger.setLevel(logging.DEBUG if enable_logging else logging.WARNING)

        # Create a console handler
        handler = logging.StreamHandler()
        # Set the handler level based on the enable_logging parameter
        handler.setLevel(logging.DEBUG if enable_logging else logging.WARNING)

        # Create a formatter
        formatter = logging.Formatter('%(message)s')

        # Add the formatter to the handler
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

        # Initialize counters for overall first and second serves and points won
        overall_first_serves = 0
        overall_second_serves = 0
        overall_first_serve_points_won = 0
        overall_second_serve_points_won = 0

        # Get specific match data for the player if a match_id is provided
        match_data = self.db.match_manager.get_match(match_id) if match_id else None

        # Get all matches for the player if no match_id is provided
        matches_data = [match_data] if match_data else self.db.match_manager.get_matches(player_name)

        # Loop over all matches
        for match_data in matches_data:

            try:
                # Convert the raw data into a Match instance
                match_instance = Match.from_record(match_data)
            except TypeError:
                # If the data is already a Match instance, use it directly
                match_instance = match_data

            # Determine the player's team
            player_team = match_instance.players[:2] if player_name in [player.name for player in match_instance.players[:2]] else match_instance.players[2:]
            logger.debug(f"Player's team: {[player.name for player in player_team]}")

            # Map player numbers to player names
            player_number_to_name = {i+1: player.name for i, player in enumerate(match_instance.players)}
            logger.debug(f"Player numbers to names mapping: {player_number_to_name}")

            # Loop over all sets in the match
            for set_instance in match_instance.sets:
                # Loop over all games in the set
                for game_index, game_instance in enumerate(set_instance.games):
                    # Initialize counters for first and second serves and points won for the current game
                    first_serves = 0
                    second_serves = 0
                    first_serve_points_won = 0
                    second_serve_points_won = 0

                    # Determine the serving player
                    serving_player_number = set_instance.serve_order[game_index % len(set_instance.serve_order)]
                    serving_player_name = player_number_to_name[serving_player_number]
                    logger.debug(f"Serving player: {serving_player_name}")

                    # If the serving player is the player of interest, count the serves and points
                    if serving_player_name == player_name:
                        logger.debug(f"Serving player is the player of interest")
                        # Get the player numbers for the player's team
                        server_team_numbers = [i+1 for i, player in enumerate(player_team)]
                        # Get the player numbers for the opponent team
                        opponent_team_numbers = [i+1 for i, player in enumerate(match_instance.players) if player not in player_team]
                        # Loop over all points in the game
                        for score, point_instance in game_instance.points.items():
                            # If the serve type is "e", it's a first serve
                            if point_instance.serve_type == "e":
                                first_serves += 1
                                overall_first_serves += 1
                                logger.debug(f"First serve point instance: {point_instance}")
                                # If the point was won by the server's team, add it to the first serve points won
                                if (point_instance.category in ["Winner", "Forced Winner"] and point_instance.player in server_team_numbers) or (point_instance.category == "Unforced Error" and point_instance.player in opponent_team_numbers):
                                    logger.debug(f"Point added to first serve count because: {point_instance.category}")
                                    first_serve_points_won += 1
                                    overall_first_serve_points_won += 1
                            # If the serve type is "t", it's a second serve
                            elif point_instance.serve_type == "t":
                                second_serves += 1
                                overall_second_serves += 1
                                logger.debug(f"Second serve point instance: {point_instance}")
                                # If the point was won by the server's team, add it to the second serve points won
                                if (point_instance.category in ["Winner", "Forced Winner"] and point_instance.player in server_team_numbers) or (point_instance.category == "Unforced Error" and point_instance.player in opponent_team_numbers):
                                    logger.debug(f"Point added to second serve count because: {point_instance.category}")
                                    second_serve_points_won += 1
                                    overall_second_serve_points_won += 1

                        # Calculate serve percentages for the game
                        first_serve_percentage_game = (first_serve_points_won / first_serves) * 100 if first_serves != 0 else 0
                        second_serve_percentage_game = (second_serve_points_won / second_serves) * 100 if second_serves != 0 else 0

                        logger.debug(f"First serve percentage for {player_name} in game {game_index + 1}: {first_serve_percentage_game}%")
                        logger.debug(f"Second serve percentage for {player_name} in game {game_index + 1}: {second_serve_percentage_game}%")

            # Calculate overall serve percentages
            first_serve_percentage = (overall_first_serve_points_won / overall_first_serves) * 100 if overall_first_serves != 0 else 0
            second_serve_percentage = (overall_second_serve_points_won / overall_second_serves) * 100 if overall_second_serves != 0 else 0

            logger.debug(f"Overall first serve percentage for {player_name}: {first_serve_percentage}%")
            logger.debug(f"Overall second serve percentage for {player_name}: {second_serve_percentage}%")

            # Return the overall first and second serve percentages
            return first_serve_percentage, second_serve_percentage
