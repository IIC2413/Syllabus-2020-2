''' 
This is our database
It manages the relations, queries and data
It has a single buffer that the relations can use to load the pages from disk
It checks that the relations are of correct type
'''

from pageNew import *
from buffer import *
from relation import *

# The buffer used by our database, and all of tis relations
Buffer = Buffer()

# The relation dictionary indexed by relation name
Relations = {}

# This is what 'CREATE TABLE R(a int, b int, c text)' does here attributes = ['a','b','c'], types = ['int','int','str']
# buff is the buffer that the table has access to; this is set to be the one used by the database
def create_table(rName, attributes, types, buff = Buffer):
    # Creates a relation with rName, and attributes as its attributes with respective types

    # First we check that the relation does not exist
    if (rName in Relations.keys()):
        print('Relation already exists')
        return False

    Rel = Relation(rName, attributes, types, buff)
    Relations[rName] = Rel

    # If all went well e return True
    return True

# This is what 'SELECT * FROM R' does
def all_tuples(R):
    R = Relations[R]

    R.open()

    while (R.has_next()):
        print(R.next())

    R.close()

# This is what 'SELECT * FROM R WHERE a = x' does
def filtered_tuples(R,cond):
    # Here cond is just a single attribute equality
    # cond is if the form 'attr = value'

    pass

def cross(R, S):
    # Performs the cross product of the two relations
    # Assumes that R is not equal to S, otherwise it will not work properly -- for bonus, implement iterators properly


    R = Relations[R]
    S = Relations[S]

    R.open()

    while (R.has_next()):
        tupR = R.next()
        S.open()
        while (S.has_next()):
            print(tupR, S.next())
        S.close()

    R.close()

    # End of the cross product
    return True

# SELECT * FROM R,S WHERE R.attrib = S.attrib
def nested_loop_join(R,S,attrib):
    # Performs a join on the attribute attrib
    pass



# SELECT * FROM R,S WHERE R.attrib = S.attrib
def block_nested_loop_join(R,S,attrib):
    # For bonus b)
    pass


# Test cases:
'''
create_table('R',['a','b'],['int','int'])

create_table('S',['b','c'],['int','int'])

cross('R','S')

all_tuples('R')

all_tuples('S')

filtered_tuples('R','a = 1')

nested_loop_join('R','S','b')
'''