import contextlib
from pypadel import *
import sqlite3


class PointStatistics:
    def __init__(self, conn):
        self.conn = conn

    def _get_sql_query(self, player_name, match_id=None, recent_n=None):
        parameters = []

        base_query = "SELECT raw_input FROM matches WHERE "

        # If match_id is provided, prioritize it
        if match_id:
            base_query += "id = ?"
            parameters.append(match_id)
            base_query += (
                " AND (player_1 = ? OR player_2 = ? OR player_3 = ? OR player_4 = ?)"
            )
            parameters.extend([player_name, player_name, player_name, player_name])
        else:
            base_query += (
                "(player_1 = ? OR player_2 = ? OR player_3 = ? OR player_4 = ?)"
            )
            parameters.extend([player_name, player_name, player_name, player_name])
            if recent_n:
                base_query += " ORDER BY date DESC LIMIT ?"
                parameters.append(recent_n)

        return base_query, tuple(parameters)

    def get_shot_distribution(
        self, player_name, match_id=None, recent_n=None, as_percentage=False
    ):
        # Define the categories
        categories = ["Unforced Error", "Winner", "Forced Winner", "Total"]

        # Initialize a dictionary to count shot-category combinations
        detailed_shot_distribution = {
            shot: {category: 0 for category in categories}
            for shot in Point.shot.values()
        }

        try:
            query, params = self._get_sql_query(player_name, match_id, recent_n)
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, params)
                all_raw_inputs = cursor.fetchall()

                for raw_input_tuple in all_raw_inputs:
                    raw_input = raw_input_tuple[0].split(",")
                    player_number = self._get_player_number(
                        player_name, raw_input_tuple[0]
                    )
                    for raw_point in raw_input:
                        point_instance = Point(raw_point)
                        if point_instance.player == player_number:
                            # Increment the total shot count
                            detailed_shot_distribution[point_instance.shot_type][
                                "Total"
                            ] += 1

                            # Increment the specific category count
                            detailed_shot_distribution[point_instance.shot_type][
                                point_instance.category
                            ] += 1

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

        # Convert the nested dictionary to a pandas DataFrame
        df = pd.DataFrame(detailed_shot_distribution).T

        # Convert raw counts to percentages if as_percentage is True
        if as_percentage:
            for shot in Point.shot.values():
                total_shots = detailed_shot_distribution[shot]["Total"]
                if total_shots != 0:  # To avoid dividing by zero
                    for category in categories[:-1]:  # Exclude "Total"
                        percentage_val = (df.at[shot, category] / total_shots) * 100
                        df.at[shot, category] = f"{round(percentage_val)}%"
                else:
                    for category in categories[:-1]:  # Exclude "Total"
                        df.at[shot, category] = "0%"

        return df

    def get_direction_distribution(
        self, player_name, match_id=None, recent_n=None, as_percentage=False
    ):
        # Define the categories
        categories = ["Unforced Error", "Winner", "Forced Winner", "Total"]

        # Initialize a dictionary to count direction-category combinations
        detailed_direction_distribution = {
            direction: {category: 0 for category in categories}
            for direction in Point.direction.values()
        }

        try:
            query, params = self._get_sql_query(player_name, match_id, recent_n)
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, params)
                all_raw_inputs = cursor.fetchall()

                for raw_input_tuple in all_raw_inputs:
                    raw_input = raw_input_tuple[0].split(",")
                    player_number = self._get_player_number(
                        player_name, raw_input_tuple[0]
                    )
                    for raw_point in raw_input:
                        point_instance = Point(raw_point)
                        if point_instance.player == player_number:
                            # Increment the total direction count
                            detailed_direction_distribution[point_instance.direction][
                                "Total"
                            ] += 1

                            # Increment the specific category count
                            detailed_direction_distribution[point_instance.direction][
                                point_instance.category
                            ] += 1

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

        # Convert the nested dictionary to a pandas DataFrame
        df = pd.DataFrame(detailed_direction_distribution).T

        # Convert raw counts to percentages if as_percentage is True
        if as_percentage:
            for direction in Point.direction.values():
                total_directions = detailed_direction_distribution[direction]["Total"]
                if total_directions != 0:  # To avoid dividing by zero
                    for category in categories[:-1]:  # Exclude "Total"
                        percentage_val = (
                            df.at[direction, category] / total_directions
                        ) * 100
                        df.at[direction, category] = f"{round(percentage_val)}%"
                else:
                    for category in categories[:-1]:  # Exclude "Total"
                        df.at[direction, category] = "0%"

        return df

    def get_shot_direction_distribution(
        self, player_name, match_id=None, recent_n=None, as_percentage=False
    ):
        # Define the categories
        categories = ["Unforced Error", "Winner", "Forced Winner", "Total"]

        # Initialize a dictionary to count shot-direction-category combinations
        shot_direction_keys = [
            (shot, direction)
            for shot in Point.shot.values()
            for direction in Point.direction.values()
        ]
        detailed_shot_direction_distribution = {
            (shot, direction): {category: 0 for category in categories}
            for shot, direction in shot_direction_keys
        }

        try:
            query, params = self._get_sql_query(player_name, match_id, recent_n)
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, params)
                all_raw_inputs = cursor.fetchall()

                for raw_input_tuple in all_raw_inputs:
                    raw_input = raw_input_tuple[0].split(",")
                    player_number = self._get_player_number(
                        player_name, raw_input_tuple[0]
                    )
                    for raw_point in raw_input:
                        point_instance = Point(raw_point)
                        if point_instance.player == player_number:
                            # Increment the total shot-direction count
                            detailed_shot_direction_distribution[
                                (point_instance.shot_type, point_instance.direction)
                            ]["Total"] += 1

                            # Increment the specific category count
                            detailed_shot_direction_distribution[
                                (point_instance.shot_type, point_instance.direction)
                            ][point_instance.category] += 1

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

        # Convert the nested dictionary to a pandas DataFrame
        df = pd.DataFrame(detailed_shot_direction_distribution).T

        # Convert raw counts to percentages if as_percentage is True
        if as_percentage:
            for shot, direction in shot_direction_keys:
                total_combinations = detailed_shot_direction_distribution[
                    (shot, direction)
                ]["Total"]
                if total_combinations != 0:  # To avoid dividing by zero
                    for category in categories[:-1]:  # Exclude "Total"
                        percentage_val = (
                            df.at[(shot, direction), category] / total_combinations
                        ) * 100
                        df.at[(shot, direction), category] = f"{round(percentage_val)}%"
                else:
                    for category in categories[:-1]:  # Exclude "Total"
                        df.at[(shot, direction), category] = "0%"

        return df

    def _get_player_number(self, player_name: str, raw_input: str):
        # Retrieve the player's number based on a match raw_input and player's name
        with contextlib.closing(self.conn.cursor()) as cursor:
            cursor.execute(
                """
                SELECT CASE
                    WHEN player_1 = ? THEN 1
                    WHEN player_2 = ? THEN 2
                    WHEN player_3 = ? THEN 3
                    WHEN player_4 = ? THEN 4
                END AS player_number 
                FROM matches 
                WHERE raw_input = ?
            """,
                (player_name, player_name, player_name, player_name, raw_input),
            )

            return cursor.fetchone()[0]

    def _process_point(
        self, point_instance, player_team_number, is_player_in_team_1, stats
    ):
        # logic for total points won needs to be tested and verified
        if is_player_in_team_1:
            relevant_teams = ({1, 2}, {3, 4})
        else:
            relevant_teams = ({3, 4}, {1, 2})

        if point_instance.player == player_team_number:  # Specific player's action
            if point_instance.category == "Unforced Error":
                stats["total_points_lost"] += 1
                stats["unforced_errors"] += 1

            elif point_instance.category == "Winner":
                stats["total_points_won"] += 1
                stats["winners"] += 1

            elif point_instance.category == "Forced Winner":
                stats["total_points_won"] += 1
                stats["forced_winners"] += 1

        elif point_instance.player in relevant_teams[0]:  # Player's teammate's action
            if point_instance.category == "Unforced Error":
                stats["total_points_lost"] += 1

            # No addition to "total_points_won" as only the specific player's winners and forced winners are considered in the "correct_get_point_statistics()"

        elif point_instance.player in relevant_teams[1]:  # Opponent's team
            if point_instance.category in ["Winner", "Forced Winner"]:
                stats["total_points_lost"] += 1

    def get_point_statistics(self, player_name, match_id=None, recent_n=None):
        stats = {
            "winners": 0,
            "unforced_errors": 0,
            "forced_winners": 0,
            "total_points_lost": 0,
            "total_points_won": 0,
            "raw_inputs_for_lost_points": [],
        }

        try:
            query, params = self._get_sql_query(player_name, match_id, recent_n)

            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, params)
                all_raw_inputs = cursor.fetchall()

                for raw_input_tuple in all_raw_inputs:
                    raw_input = raw_input_tuple[0].split(",")
                    player_team_number = self._get_player_number(
                        player_name, raw_input_tuple[0]
                    )
                    is_player_in_team_1 = player_team_number in [1, 2]

                    for raw_point in raw_input:
                        # Check if the first character of raw_point is a digit
                        if not raw_point[0].isdigit():
                            continue
                        point_instance = Point(raw_point)
                        self._process_point(
                            point_instance,
                            player_team_number,
                            is_player_in_team_1,
                            stats,
                        )

                if recent_n:
                    for key in stats:
                        if key != "raw_inputs_for_lost_points":
                            stats[key] /= recent_n

                return stats

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            return {}
