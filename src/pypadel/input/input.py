from pypadel.match_mechanics import Player, Match, Point, InvalidPoint
from pypadel.match_mechanics.point_mappings import (
    POINT_STRUCTURE,
    FORCED_WINNER_POINT_STRUCTURE,
    serve_type,
    cat,
    side,
    shot,
    direction,
)
import pandas as pd
from datetime import datetime


import os


class InputManager:
    def __init__(self, match_instance):
        self.match = match_instance
        self.input_history = []  # Stack to maintain history of inputs

        date_str = self.match.date
        team1_names = "and".join(
            [self.match.players[0].name, self.match.players[1].name]
        )
        team2_names = "and".join(
            [self.match.players[2].name, self.match.players[3].name]
        )
        match_type = self.match.__class__.__name__

        # Construct the log file name with team information
        self.log_file_path = (
            f"data/logs/match_log_{date_str}_{team1_names}_vs_{team2_names}.log"
        )

        # Check if the log file already exists
        if not os.path.exists(self.log_file_path):
            # If not, create it and write the match details on the first line
            with open(self.log_file_path, "w") as log_file:
                match_details = f"{date_str},{self.match.tournament},{self.match.r},{self.match.adv_game},{self.match.players[0].name},{self.match.players[1].name},{self.match.players[2].name},{self.match.players[3].name},{match_type},"
                log_file.write(match_details)

    def process_input(self, user_input):
        # Log the input to a file for recovery
        with open(self.log_file_path, "a") as log_file:
            log_file.write(user_input + ",")  # Write the input followed by a newline

        if user_input == "u":
            self.undo_last_input()
            return

        self.input_history.append(user_input)  # Add the processed input to history
        self.match.process(user_input)

    def undo_last_input(self):
        if self.input_history:
            self.input_history.pop()  # Remove the last input
            self.reprocess_match()  # Reprocess the match with the updated history

    def reprocess_match(self):
        # Save the current match configuration (like players, match type, etc.)
        match_config = {
            "players": self.match.players,
            "date": self.match.date,
            "tournament": self.match.tournament,
            "r": self.match.r,
            "adv_game": self.match.adv_game,
        }

        # Reinitialize the match instance
        self.match.__init__(**match_config)

        # Reprocess each input in the history
        for input_item in self.input_history:
            self.match.process(input_item)


def get_valid_date():
    while True:
        date_str = input("Date of the Tournament (format: YYYY-MM-DD): ")
        try:
            # Attempt to convert the date string to a datetime object
            valid_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return valid_date
        except ValueError:
            # If parsing fails, notify the user and prompt again
            print("Invalid date format. Please enter in the format YYYY-MM-DD.")


def start_match(
    point_structure=POINT_STRUCTURE,
    forced_winner_point_structure=FORCED_WINNER_POINT_STRUCTURE,
):
    date = get_valid_date()
    tournament = input("Tournament name: ")
    r = input("Round: ")
    adv_game = input("Are the games played with advantage - (Y) yes or (N) no: ") in [
        "y",
        "Y",
    ]
    p1 = Player(input("Name player 1: "))
    p2 = Player(input("Name player 2: "))
    p3 = Player(input("Name player 3: "))
    p4 = Player(input("Name player 4: "))
    m_type = input("Match_type: ")

    players = [p for p in [p1, p2, p3, p4]]

    m = Match.create(
        int(m_type),
        players=players,
        date=date,
        tournament=tournament,
        r=r,
        adv_game=adv_game,
    )

    # Use the InputManager for processing inputs
    input_manager = InputManager(m)

    # Acknowledge the input of match details and display the match info
    print("Thanks for the information, this is the match info:")
    print(m)

    while True:
        x = input("Point: ")  # Prompt the user for point input
        if x == "Q":
            break
        while not input_ok(x, point_structure, forced_winner_point_structure):
            if x == "Q":
                break
            x = input(
                f"{x} is an invalid input. Try again: "
            )  # Prompt again if input is invalid

        # Process the input using the InputManager
        input_manager.process_input(x)

    return m


def input_ok(
    x,
    point_structure=POINT_STRUCTURE,
    forced_winner_point_structure=FORCED_WINNER_POINT_STRUCTURE,
):
    if x == "":
        print(f"No input")
        return False
    # x = x.lower() removed this as some inputs are case sensitive in our generated tests, could be revised at some point
    pl = {"1", "2", "3", "4"}
    if x[0] == "#" and x[1] in pl:
        return True
    if x[0] == "!":
        return True
    # Allow "u" as a valid input for undoing
    if x.lower() == "u":
        return True

    min_length = max(s.stop for s in point_structure.values())
    if len(x) < min_length:
        print("Input length is too short")
        return False
    point_data = {attr: x[s] for attr, s in point_structure.items()}
    if point_data["serve_type"] not in serve_type:
        print(f"Serve type is incorrect -> got {point_data['serve_type']}")
        return False
    if point_data["player"] not in pl:
        print(f"Player is incorrect -> got {point_data['player']}")
        return False
    if point_data["category"] not in cat:
        print(
            f"Category is incorrect -> got {point_data['category']} which is not in {cat}"
        )
        return False
    if point_data["side"] not in side:
        print(
            f"The side is incorrect -> got {point_data['side']} which is not in {side}"
        )
        return False
    if point_data["shot_type"] not in shot:
        print(
            f"Shot is incorrect -> got {point_data['shot_type']} which is not in {shot}"
        )
        return False
    if point_data["direction"] not in direction:
        print(
            f"Direction is incorrect -> got {point_data['direction']} which is not in {direction}"
        )
        return False
    if point_data["category"] == "f":
        min_length_forced = max(s.stop for s in forced_winner_point_structure.values())
        if len(x) < min_length_forced:
            print("Input length is too short for a forced winner point")
            return False
        forced_winner_data = {
            attr: x[s] for attr, s in forced_winner_point_structure.items()
        }
        if forced_winner_data["player2"] not in pl:
            print(
                f"Player making the forced error is incorrect -> got {forced_winner_data['player2']}"
            )
            return False
        if forced_winner_data["side2"] not in side:
            print(
                f"The side of player making the forced error is incorrect -> got {forced_winner_data['side2']} which is not in {side}"
            )
            return False
        if forced_winner_data["shot_type_2"] not in shot:
            print(
                f"Shot of player making the forced error is incorrect -> got {forced_winner_data['shot_type_2']} which is not in {shot}"
            )
            return False

    # Try to initialize a Point object with the input string
    point = Point(x)
    # If the Point object becomes an InvalidPoint, then the input is not valid
    if isinstance(point, InvalidPoint):
        print(f"Invalid point input: {x}")
        return False

    return True
