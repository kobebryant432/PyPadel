from pypadel.match_mechanics import Player, Match
import pandas as pd
from datetime import datetime


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


def start_match():
    date = get_valid_date()
    tournament = input("Tournament name: ")
    r = input("Round :")
    adv_game = input("Are the games played with advantage - (Y) yes or (N) no:") in [
        "y",
        "Y",
    ]
    p1 = Player(input("Name player 1: "))
    p2 = Player(input("Name player 2: "))
    p3 = Player(input("Name player 3: "))
    p4 = Player(input("Name player 4: "))
    m_type = input("Match_type")

    players = [p for p in [p1, p2, p3, p4]]

    m = Match.create(
        int(m_type),
        players=players,
        date=date,
        tournament=tournament,
        r=r,
        adv_game=adv_game,
    )

    while True:
        x = input()
        if x == "Q":
            break
        while not input_ok(x):
            if x == "Q":
                break
            x = input(f"{x} is an invalid input. Try again")
        m.process(x)
    return m


def input_ok(x):
    if x == "":
        print(f"No input")
        return False
    x = x.lower()
    serve = {"1","2"}
    pl = {"1", "2", "3", "4"}
    cat = {"f", "u", "w"}
    side = {"fh", "bh", "hi", "hd"}
    shot = {"v", "o", "n", "g", "r", "l", "s", "V", "k", "b", "j", "z", "f"}
    direction = {"c", "p", "n", "l", "m", "d", "k", "f", "g"}
    if x[0] == "#" and x[1] in pl:
        return True
    if x[0] == "!":
        return True
    if len(x) < 7:
        print("Input lenght is to short")
        return False
    if x[0] not in serve:
        print(f"serve is incorrect -> got {x[0]}")
        return False
    if x[1] not in pl:
        print(f"Player is incorrect -> got {x[1]}")
        return False
    if x[2] not in cat:
        print(f"Category is incorrect -> got {x[2]} which is not in {cat}")
        return False
    if x[3:5] not in side:
        print(f"The side is incorrect -> got {x[3:5]} which is not in {side}")
        return False
    if x[5] not in shot:
        print(f"Shot is incorrect -> got {x[5]} which is not in {shot}")
        return False
    if x[6] not in direction:
        print(f"Direction is incorrect -> got {x[6]} which is not in {direction}")
        return False
    if x[2] == "f":
        if len(x) < 11:
            print("Input lenght is to short")
            return False
        if x[7] not in pl:
            print(f"Player making the forced error is incorrect -> got {x[1]}")
            return False
        if x[8:10] not in side:
            print(
                f"The side of player making the forced error is incorrect -> got {x[8:10]} which is not in {side}"
            )
            return False
        if x[10] not in shot:
            print(
                f"Shot of player making the forced error is incorrect -> got {x[10]} which is not in {shot}"
            )
            return False
    return True
