from input import *
from database import database
import pickle

#Some examples!

#Example 1 - To track a match using python and save result to excel

#m = start_match()
#Export the match statistics of the analysed match.
#m.export()
#Export the 'raw' data of this match to be added to a database input excel later.
#m.export_raw('in/my_first_match.xlsx')
    
#Example 2 - Loading a db
# db = database('test') 
# db.load_db('in/input_clean.xlsx') 
# db.export_all()

# Initialize your database
M_1000 = database('P1000 Men') 
# Load the input dataset - note that if there is incorrect input you will need to correct it.
M_1000.load_db('in/input_clean.xlsx', sheet_name='Heren 1000')

#Let's say you want to add a match to the db. For example your newly tracked match m:
#M_1000.add_match(m) # Add match m
M_1000.add_match(M_1000.matches['match'][0]) # A working example which adds a copy of the first match to the db.

#Save the raw data from your input 
#-> Good to do if you made corrections or if you added a match. Corrections will be made.
M_1000.export_all_raw('in/input.xlsx',sheetname='Heren 1000')
#Export all the analysis of each match in the database.
M_1000.export_all()

#Another way to save a db is to save the whole db (not only the raw-data), this has the advantage of not having to reload all the input.
M_1000.save_db('in/m1000.pkl')

#To load a saved db
with open('in/m1000.pkl','rb') as inp:
    M_1000 = pickle.load(inp)

#To get a specific match - get the (n-1) th match of the db. Can get last or second last with -1 (-2)
p = M_1000.get_match(0)