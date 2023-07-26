from pypadel.match_mechanics import Player, Match
import pandas as pd


def start_match():
    date = input("Date of the Tournament: ")
    tournament = input("Tournament name: ")
    r = input("Round :")
    p1 = Player(input("Name player 1: "))
    p2 = Player(input("Name player 2: "))
    p3 = Player(input("Name player 3: "))
    p4 = Player(input("Name player 4: "))
    m_type = input("Match_type")

    players = [p for p in [p1, p2, p3, p4]]

    m = Match.create(
        int(m_type), players=players, date=date, tournament=tournament, r=r
    )

    while True:
        x = input()
        if x == "Q":
            break
        while not input_ok(x):
            if x == "Q":
                break
            x = input(f"{x} is an invallid input. Try again")
        m.process(x)
    return m


def input_ok(x):
    if x == "":
        print(f"No input")
        return False
    x = x.lower()
    pl = {"1", "2", "3", "4"}
    cat = {"f", "u", "w"}
    side = {"fh", "bh", "hi", "hd"}
    shot = {"v", "o", "n", "g", "r", "l", "s", "V", "k", "b", "j", "z", "f"}
    direction = {"c", "p", "n", "l", "m", "d", "k", "f", "g"}
    if x[0] == "#" and x[1] in pl:
        return True
    if x[0] == "!":
        return True
    if len(x) < 6:
        print("Input lenght is to short")
        return False
    if x[0] not in pl:
        print(f"Player is incorrect -> got {x[0]}")
        return False
    if x[1] not in cat:
        print(f"Category is incorrect -> got {x[1]} which is not in {cat}")
        return False
    if x[2:4] not in side:
        print(f"The side is incorrect -> got {x[2:4]} which is not in {side}")
        return False
    if x[4] not in shot:
        print(f"Shot is incorrect -> got {x[4]} which is not in {shot}")
        return False
    if x[5] not in direction:
        print(f"Direction is incorrect -> got {x[5]} which is not in {direction}")
        return False
    if x[1] == "f":
        if len(x) < 10:
            print("Input lenght is to short")
            return False
        if x[6] not in pl:
            print(f"Player making the forced error is incorrect -> got {x[0]}")
            return False
        if x[7:9] not in side:
            print(
                f"The side of player making the forced error is incorrect -> got {x[7:9]} which is not in {side}"
            )
            return False
        if x[9] not in shot:
            print(
                f"Shot of player making the forced error is incorrect -> got {x[9]} which is not in {shot}"
            )
            return False
    return True
