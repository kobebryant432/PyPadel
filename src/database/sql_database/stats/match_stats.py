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

        # Draw the labels in the center
        for label, position in positions["Labels"].items():
            x, y = position
            draw.text((x, y), label, font=font, fill="black", anchor="ms")

        # Save the image to the desired output path
        img.save(output_path)

        return output_path
