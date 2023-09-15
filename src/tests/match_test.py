"""
# src/tests/test_matches.py

This script is used to test the functionality of the Match class in the pypadel module. It includes tests for different types of matches (tie, 3 sets, proset) with different game advantages.

To use this script, run it from the command line or from a Jupyter notebook. The script will automatically run all the tests and log the results in 'pypadel_tests.log' file.

The script uses Python's unittest module for testing. Each test creates a match with four players and plays the match with randomly generated valid point strings until the match is finished. If an error occurs during the match, it is logged and the test fails.

"""

import os #nopep8
import sys #nopep8
import builtins #nopep8
from pathlib import Path #nopep8

# Add the 'src' directory to sys.path
current_working_directory = os.getcwd()  # Get the current working directory
src_path = (
    Path(current_working_directory) / "src"
)  # Construct the path to the 'src' directory
try:
    sys.path.append(str(src_path))  # Add 'src' directory to sys.path
    from pypadel import Player, Match, Point
except ModuleNotFoundError:
    src_path = src_path.parent.parent
    sys.path.append(str(src_path))
    from pypadel import Player, Match, Point

import unittest
import random
import logging

class TestMatch(unittest.TestCase):
    """
    This class contains the tests for the Match class in the pypadel module.
    """
    
    def setUp(self):
        """
        This method sets up the test environment. It is run before each test.
        """
        self.players = [Player("Player 1"), Player("Player 2"), Player("Player 3"), Player("Player 4")]
        self.point_strings = list(Point.generate_valid_point_strings())
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pypadel_tests.log')
        logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def test_match_tie(self):
        """
        This method tests a tie match with both game advantages.
        """
        for adv_game in [True, False]:
            match = Match.create(0, self.players, adv_game=adv_game)
            while not match.finished:
                point_string = random.choice(self.point_strings)
                try:
                    match.play_match([point_string])
                except Exception as e:
                    logging.error(f"Match tie with point string {point_string} and adv_game {adv_game} failed with error: {e}")
            self.assertTrue(match.finished)
            logging.info(f"Match tie with adv_game {adv_game} finished successfully with score: {match.get_set_scores()}. Match details: {str(match)}")

    def test_match_3_sets(self):
        """
        This method tests a 3 sets match with both game advantages.
        """
        for adv_game in [True, False]:
            match = Match.create(1, self.players, adv_game=adv_game)
            while not match.finished:
                point_string = random.choice(self.point_strings)
                try:
                    match.play_match([point_string])
                except Exception as e:
                    logging.error(f"3 sets match with point string {point_string} and adv_game {adv_game} failed with error: {e}")
            self.assertTrue(match.finished)
            logging.info(f"3 sets match with adv_game {adv_game} finished successfully with score: {match.get_set_scores()}. Match details: {str(match)}")

    def test_match_proset(self):
        """
        This method tests a proset match with both game advantages.
        """
        for adv_game in [True, False]:
            match = Match.create(2, self.players, adv_game=adv_game)
            while not match.finished:
                point_string = random.choice(self.point_strings)
                try:
                    match.play_match([point_string])
                except Exception as e:
                    logging.error(f"Proset match with point string {point_string} and adv_game {adv_game} failed with error: {e}")
            self.assertTrue(match.finished)
            logging.info(f"Proset match with adv_game {adv_game} finished successfully with score: {match.get_set_scores()}. Match details: {str(match)}")

if __name__ == "__main__":
    """
    This block runs the tests when the script is run from the command line or a Jupyter notebook / interactive window.
    """
    if 'ipykernel' in sys.modules:
        # Code is running in Jupyter notebook
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        # Code is running from the terminal
        unittest.main()
