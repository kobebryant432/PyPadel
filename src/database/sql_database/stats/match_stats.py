import contextlib
from pypadel import *
import sqlite3
from PIL import Image, ImageDraw, ImageFont


class MatchStats:
    def __init__(self, conn, match_id):
        self.conn = conn
        self.match_id = match_id

    def _get_match_details(self):
        query = """
        SELECT r, tournament, date, player_1, player_2, player_3, player_4, sets_score FROM matches WHERE id = ?
        """
        try:
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, (self.match_id,))
                match_data = cursor.fetchone()

                match_detail = {
                    "r": match_data[0],
                    "tournament": match_data[1],
                    "date": match_data[2],
                    "team1": [match_data[3], match_data[4]],
                    "team2": [match_data[5], match_data[6]],
                    "sets_score": match_data[7],
                }

                return match_detail

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            return None

    def _get_match_object(self):
        """
        This method retrieves the match data from the database and converts it into a Match object.

        Returns:
            Match: The Match object for the match.
        """

        # Get the match data from the database
        query = "SELECT * FROM matches WHERE id = ?"
        try:
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, (self.match_id,))
                match_record = cursor.fetchone()

                # Convert the raw data into a Match object
                if match_record:
                    match_instance = Match.from_record(match_record)
                    return match_instance

                return None

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            return None

    def _get_players_in_match(self):
        # Assuming teams are composed of player_1 and player_2 vs. player_3 and player_4
        query = """
        SELECT player_1, player_2, player_3, player_4 FROM matches
        WHERE id = ?
        """
        try:
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, (self.match_id,))
                players = cursor.fetchone()
            return players
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            return None

    def _get_sql_query_for_team(self, team_players):
        base_query = """
        SELECT raw_input FROM matches 
        WHERE id = ? AND (player_1 = ? OR player_2 = ?)
        """
        parameters = (self.match_id, team_players[0], team_players[1])
        return base_query, parameters
    
    def get_team_serve_percentages(self):
        """
        This method calculates the first and second serve percentages for each team in a match.

        Returns:
            dict: A dictionary with the first and second serve percentages for each team.
        """

        # Initialize counters for overall first and second serves and points won for each team
        serve_stats = {
            "Team 1": {"first_serves": 0, "second_serves": 0, "first_serve_points_won": 0, "second_serve_points_won": 0},
            "Team 2": {"first_serves": 0, "second_serves": 0, "first_serve_points_won": 0, "second_serve_points_won": 0}
        }

        # Get the match instance
        match_instance = self._get_match_object()

        # Map player numbers to player names
        player_number_to_name = {i+1: player.name for i, player in enumerate(match_instance.players)}

        # Determine the teams
        team1 = match_instance.players[:2]
        team2 = match_instance.players[2:]

        print(f"Team 1: {[player.name for player in team1]}")
        print(f"Team 2: {[player.name for player in team2]}")

        # Get player numbers for both teams
        team1_numbers = [1, 2]
        team2_numbers = [3, 4]


        # Loop over all sets in the match
        for set_instance in match_instance.sets:
            # Loop over all games in the set
            for game_index, game_instance in enumerate(set_instance.games):
                # Determine the serving player
                serving_player_number = set_instance.serve_order[game_index % len(set_instance.serve_order)]
                # Determine the serving team
                serving_team = "Team 1" if serving_player_number in [1, 2] else "Team 2"
                print(f"Game {game_index + 1} is being served by {serving_team}")

                # Loop over all points in the game
                for score, point_instance in game_instance.points.items():
                    # Debugging statements to understand the attributes of each point instance
                    print(f"Point {score}:")
                    print(f"  Serve Type: {point_instance.serve_type}")
                    print(f"  Category: {point_instance.category}")
                    print(f"  Player: {point_instance.player}")

                    # Determine the serving team numbers
                    serving_team_numbers = team1_numbers if serving_team == "Team 1" else team2_numbers
                    # Determine the opponent team numbers
                    opponent_team_numbers = team2_numbers if serving_team == "Team 1" else team1_numbers

                    print(f"  Serving Team Numbers: {serving_team_numbers}")
                    print(f"  Opponent Team Numbers: {opponent_team_numbers}")
                    print(f" Player {point_instance.player} is {player_number_to_name[point_instance.player]}")
                    
                    # If the serve type is "e", it's a first serve
                    if point_instance.serve_type == "e":
                        serve_stats[serving_team]["first_serves"] += 1
                        # If the point was won by the serving team, add it to the first serve points won
                        if (
                            (point_instance.category in ["Winner", "Forced Winner"] and point_instance.player in serving_team_numbers)
                            or (point_instance.category == "Unforced Error" and point_instance.player in opponent_team_numbers)
                        ):
                            serve_stats[serving_team]["first_serve_points_won"] += 1
                    # If the serve type is "t", it's a second serve
                    elif point_instance.serve_type == "t":
                        serve_stats[serving_team]["second_serves"] += 1
                        # If the point was won by the serving team, add it to the second serve points won
                        if (
                            (point_instance.category in ["Winner", "Forced Winner"] and point_instance.player in serving_team_numbers)
                            or (point_instance.category == "Unforced Error" and point_instance.player in opponent_team_numbers)
                        ):
                            serve_stats[serving_team]["second_serve_points_won"] += 1
                
                # Print the serve stats after each game to debug
                print(f"Serve stats after game {game_index + 1}:")
                for team, stats in serve_stats.items():
                    first_serve_percentage = (stats["first_serve_points_won"] / stats["first_serves"]) * 100 if stats["first_serves"] != 0 else 0
                    second_serve_percentage = (stats["second_serve_points_won"] / stats["second_serves"]) * 100 if stats["second_serves"] != 0 else 0
                    print(f"  {team}:")
                    print(f"    First Serve Percentage: {first_serve_percentage}%")
                    print(f"    Second Serve Percentage: {second_serve_percentage}%")

        # Calculate serve percentages for each team
        for team, stats in serve_stats.items():
            first_serve_percentage = (stats["first_serve_points_won"] / stats["first_serves"]) * 100 if stats["first_serves"] != 0 else 0
            second_serve_percentage = (stats["second_serve_points_won"] / stats["second_serves"]) * 100 if stats["second_serves"] != 0 else 0
            serve_stats[team]["first_serve_percentage"] = first_serve_percentage
            serve_stats[team]["second_serve_percentage"] = second_serve_percentage

        return serve_stats

    def get_match_summary(self):
        players = self._get_players_in_match()
        if not players:
            return

        team1 = players[:2]
        team2 = players[2:]

        # Initialize statistics
        stats = {
            "Team 1": {
                "Unforced Errors": 0,
                "Winners": 0,
                "Forced Winners": 0,
                "Total Points Won": 0,
                "Total Points Lost": 0,
            },
            "Team 2": {
                "Unforced Errors": 0,
                "Winners": 0,
                "Forced Winners": 0,
                "Total Points Won": 0,
                "Total Points Lost": 0,
            },
            "Total Points in the Match": 0,
        }

        query = """
        SELECT raw_input FROM matches WHERE id = ?
        """
        try:
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute(query, (self.match_id,))
                raw_data = cursor.fetchone()[0]
                raw_points = raw_data.split(",")
                stats["Total Points in the Match"] = len(raw_points)

                for raw_point in raw_points:
                    point_instance = Point(raw_point)

                    # Identify team
                    team = "Team 1" if point_instance.player in [1, 2] else "Team 2"
                    opponent_team = "Team 2" if team == "Team 1" else "Team 1"

                    # Update statistics based on point data
                    if point_instance.category == "Unforced Error":
                        stats[team]["Unforced Errors"] += 1
                        stats[opponent_team]["Total Points Won"] += 1
                        stats[team]["Total Points Lost"] += 1
                    elif point_instance.category == "Winner":
                        stats[team]["Winners"] += 1
                        stats[team]["Total Points Won"] += 1
                        stats[opponent_team]["Total Points Lost"] += 1
                    elif point_instance.category == "Forced Winner":
                        stats[team]["Forced Winners"] += 1
                        stats[team]["Total Points Won"] += 1
                        stats[opponent_team]["Total Points Lost"] += 1

                # Compute average unforced errors and winners per game
                for team in ["Team 1", "Team 2"]:
                    avg_unforced_errors_per_game = stats[team]["Unforced Errors"] / (
                        stats["Total Points in the Match"] / 5.5
                    )
                    avg_winners_per_game = (
                        stats[team]["Winners"] + stats[team]["Forced Winners"]
                    ) / (stats["Total Points in the Match"] / 5.5)

                    stats[team]["Avg Unforced Errors/Game"] = round(
                        avg_unforced_errors_per_game, 2
                    )
                    stats[team]["Avg Winners/Game"] = round(avg_winners_per_game, 2)

        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

        return stats

    def export_summary_to_image(
        self, summary, template_path="data/img/template.png", output_path=None
    ):
        # Load the template
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)

        # Assume a certain font and size
        font = ImageFont.truetype("arial.ttf", 24)

        # Get match details
        match_detail = self._get_match_details()

        # Get serve stats
        serve_stats = self.get_team_serve_percentages()

        # If no output_path is provided, construct a dynamic one
        if not output_path:
            tournament = match_detail["tournament"]
            p1 = match_detail["team1"][0]
            p3 = match_detail["team2"][0]

            # Construct the dynamic path
            output_path = f"match_summary_{tournament}_{p1}_{p3}.png"

        # Write tournament, date, and round details centered
        tournament_position = (img.width // 2, 50)
        draw.text(
            tournament_position,
            match_detail["tournament"],
            font=font,
            fill="black",
            anchor="ms",
        )

        date_position = (img.width // 2, 90)
        draw.text(
            date_position,
            match_detail["date"],
            font=font,
            fill="black",
            anchor="ms",
        )

        round_position = (img.width // 2, 130)
        draw.text(
            round_position, match_detail["r"], font=font, fill="black", anchor="ms"
        )

        # Sets score position and drawing
        sets_score_position = (img.width // 2, 220)
        draw.text(
            sets_score_position,
            match_detail["sets_score"],
            font=font,
            fill="black",
            anchor="ms",
        )

        # Adjusted positions for team1 and team2 player names to make space for sets_score
        team1_player1_position = (img.width * 1 / 4, 200)
        draw.text(
            team1_player1_position,
            match_detail["team1"][0],
            font=font,
            fill="black",
            anchor="ms",
        )

        team1_player2_position = (img.width * 1 / 4, 240)
        draw.text(
            team1_player2_position,
            match_detail["team1"][1],
            font=font,
            fill="black",
            anchor="ms",
        )

        team2_player1_position = (img.width * 3 / 4, 200)
        draw.text(
            team2_player1_position,
            match_detail["team2"][0],
            font=font,
            fill="black",
            anchor="ms",
        )

        team2_player2_position = (img.width * 3 / 4, 240)
        draw.text(
            team2_player2_position,
            match_detail["team2"][1],
            font=font,
            fill="black",
            anchor="ms",
        )

        # Define positions for the stats, adjusting positions for Team1 and Team2,
        # and adding center positions for the labels
        positions = {
            "Team 1": {
                "Unforced Errors": (img.width * 1 / 4, 300),
                "Winners": (img.width * 1 / 4, 340),
                "Forced Winners": (img.width * 1 / 4, 380),
                "Total Points Won": (img.width * 1 / 4, 420),
                "Avg Unforced Errors/Game": (img.width * 1 / 4, 460),
                "Avg Winners/Game": (img.width * 1 / 4, 500),
            },
            "Team 2": {
                "Unforced Errors": (img.width * 3 / 4, 300),
                "Winners": (img.width * 3 / 4, 340),
                "Forced Winners": (img.width * 3 / 4, 380),
                "Total Points Won": (img.width * 3 / 4, 420),
                "Avg Unforced Errors/Game": (img.width * 3 / 4, 460),
                "Avg Winners/Game": (img.width * 3 / 4, 500),
            },
            "Labels": {
                "Unforced Errors": (img.width // 2, 300),
                "Winners": (img.width // 2, 340),
                "Forced Winners": (img.width // 2, 380),
                "Total Points Won": (img.width // 2, 420),
                "Avg Unforced Errors/Game": (img.width // 2, 460),
                "Avg Winners/Game": (img.width // 2, 500),
            },
        }

        # Define positions for the serve stats
        serve_positions = {
            "Team 1": {
                "first_serve_percentage": (img.width * 1 / 4, 540),
                "second_serve_percentage": (img.width * 1 / 4, 580),
            },
            "Team 2": {
                "first_serve_percentage": (img.width * 3 / 4, 540),
                "second_serve_percentage": (img.width * 3 / 4, 580),
            },
            "Labels": {
                "%pts won 1st serve": (img.width // 2, 540),
                "%pts won 2nd serve": (img.width // 2, 580),
            },
        }

        # Draw the stats onto the image at their respective positions without labels
        for category, values in summary.items():
            if category in ["Team 1", "Team 2"]:
                for key, value in values.items():
                    if (
                        key in positions[category]
                    ):  # Check if the key exists in positions dictionary
                        x, y = positions[category][key]
                        draw.text(
                            (x, y), str(value), font=font, fill="black", anchor="ms"
                        )

        # Draw the serve stats onto the image at their respective positions without labels
        for team, stats in serve_stats.items():
            for key, value in stats.items():
                print(key)
                print(value)
                if key in serve_positions[team]:  # Check if the key exists in serve_positions dictionary
                    x, y = serve_positions[team][key]
                    draw.text(
                        (x, y), f"{value:.2f}%", font=font, fill="black", anchor="ms"
                    )
        
        # Draw the labels in the center
        for label, position in positions["Labels"].items():
            x, y = position
            draw.text((x, y), label, font=font, fill="black", anchor="ms")

        # Draw the serve labels in the center
        for label, position in serve_positions["Labels"].items():
            x, y = position
            draw.text((x, y), label, font=font, fill="black", anchor="ms")

        # Save the image to the desired output path
        img.save(output_path)

        return output_path