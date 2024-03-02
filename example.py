import os  # nopep8
import sys  # nopep8
from pathlib import Path  # nopep8
import builtins

# Add the 'src' directory to sys.path
current_working_directory = os.getcwd()  # Get the current working directory
src_path = (
    Path(current_working_directory) / "src"
)  # Construct the path to the 'src' directory
sys.path.append(str(src_path))  # Add 'src' directory to sys.path

from pypadel import *
from database import *

# These point_structures can be updated if you want to add more/less attributes to the input, only these attributes will be checked.
# Easiest way is to comment out certain elements, you can't add new elements (they will not be processed). Updating the slices is not necessary.
INPUT_POINT_STRUCTURE = {
    "serve_type": slice(0, 1),
    "player": slice(1, 2),
    "category": slice(2, 3),
    "side": slice(3, 5),
    "shot_type": slice(5, 6),
    "direction": slice(6, 7),
}

INPUT_FORCED_WINNER_POINT_STRUCTURE = {
    **INPUT_POINT_STRUCTURE,
    "player2": slice(7, 8),
    "side2": slice(8, 10),
    "shot_type_2": slice(10, 11),
}

# add a data path
db_path = Path(current_working_directory) / "data" / "db"
xlsx_path = Path(current_working_directory) / "data" / "xlsx"

db = SqlDatabase.init_from_existing(db_filename=db_path / "test.db")


m = start_match(INPUT_POINT_STRUCTURE, INPUT_FORCED_WINNER_POINT_STRUCTURE)
# Export the match statistics of the analysed match.
# m.export()
# # Export the 'raw' data of this match to be added to a database input excel later.
# m.export_raw(file= 'in/local_inputs.xlsx')
db.add_match(m=m, cat=builtins.input("Fill in the Category: "))
db.export_raw()
db.close()

# Example 2 - Loading a db
# db = database('test') 4ubhnl
# db.load_db('in/input_clean.xlsx')
# db.export_all()

# Initialize your database
# D = database('P1000 Men')
# # # Load the input dataset - note that if there is incorrect input you will need to correct it.
# D.load_db('in/local_inputs.xlsx')

# #Let's say you want to add a match to the db. For example your newly tracked match m:
# #M_1000.add_match(m) # Add match m
# M_1000.add_match(M_1000.matches['match'][0]) # A working example which adds a copy of the first match to the db.

# #Save the raw data from your input
# #-> Good to do if you made corrections or if you added a match. Corrections will be made.
# M_1000.export_all_raw('in/input.xlsx',sheetname='Heren 1000')
# #Export all the analysis of each match in the database.
# M_1000.export_all()

# #Another way to save a db is to save the whole db (not only the raw-data), this has the advantage of not having to reload all the input.
# M_1000.save_db('in/m1000.pkl')

# #To load a saved db
# with open('in/m1000.pkl','rb') as inp:
#     M_1000 = pickle.load(inp)

# #To get a specific match - get the (n-1) th match of the db. Can get last or second last with -1 (-2)
# p = M_1000.get_match(0)
