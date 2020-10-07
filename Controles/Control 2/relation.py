from pageNew import *
from buffer import *
class Relation:
	# The constructor initializes the buffer
	def __init__(self, rName, aNames, aTypes, buff):
		if not(len(aNames) == len(aTypes)):
			print('Relation definition error')
			return

		self.buffer = buff # The buffer that the relation uses; this is passed to the relation by the database
		self.rName = rName # Relation name
		self.attributes = aNames # Names of our attributes; this should be a list
		self.types = aTypes # Type of each attribute; for now we support only int and text, where text can not have spaces
		self.numAttrib = len(self.attributes) # number of attributes
		self.root_page = self.rName + '-1' # Name of the Root page = relationName-1 (e.g. for R R-1)
		# We make sure that the root page exists		
		self.create_root()
		self.current_page = None # The page we are currently on; before operning we are not doing anything
		self.current_pos = None # Current position on the current_page; before opening None

	def create_root(self):
		# Next, we create the root page if it does not exist already (not to have inconsistencies later)
		# Note that the only communication with the disk is through the buffer
		self.buffer.create_page(self.root_page)


	def open(self):
		# Resets the cursor to the beginning
		self.current_page = self.root_page
		self.current_pos = -1

	def has_next(self):
		# Returns True/False depending on whether there is a next tuple
		# It does not modify self.current_page, nor self.current_pos
		# The next function does this looping recursively
		return self.find_next_pos(self.current_page,self.current_pos)

	def find_next_pos(self, currPage, currPos):
		# Uses the same logic as get_next_pos(), but without changing self.current_page, nor self.current_pos

		if not(currPage):
			return False

		# We need to advance by one first and do all the checks (we consumed the last tuple in next())
		currPos += 1

		# If we came to the end, we need to move onto the next page; 4 should be changed by PAGE_SIZE constant
		if currPos == 5:
			# Get the page we are working with
			page = self.buffer.get_page(currPage)
			next_page = page.next
			if next_page == '<NULL>':
				# We came to an end
				return False
			else:
				# If not, we obtain the next page name
				currPage = next_page
				# Set the position to zero
				currPos = 0

		# Now we roll

		page = self.buffer.get_page(currPage)

		# If the page position is empty, we call has_next again recursively:
		if page.get_element_from_page(currPos) == '<EMPTY>':
			return self.find_next_pos(currPage,currPos)
		
		return True


	def get_next_pos(self):
		# returns true if there is a next tuple
		# It also positions the "pointers" self.current_page and self.current_tuple over the next tuple
		# That is, it will advance the self.current_page and self.current_pos to the one with the next tuple

		if not(self.current_page):
			print('Iterator is closed')
			return False

		# We need to advance by one first and do all the checks (we consumed the last tuple in next())
		self.current_pos += 1

		# If we came to the end, we need to move onto the next page; 4 should be changed by PAGE_SIZE constant
		if self.current_pos == 5:
			# Get the page we are working with
			page = self.buffer.get_page(self.current_page)
			next_page = page.next
			if next_page == '<NULL>':
				# We came to an end
				return False
			else:
				# If not, we obtain the next page name
				self.current_page = next_page
				# Set the position to zero
				self.current_pos = 0

		# Now we roll
		pname = self.current_page
		pos = self.current_pos

		page = self.buffer.get_page(pname)

		# If the page position is empty, we call has_next again recursively:
		if page.get_element_from_page(pos) == '<EMPTY>':
			return self.get_next_pos()
		
		return True


		
	def next(self):
		# returns the next tuple; if it does not exist returns none
		# When called, will advance the self.current_page and self.current_pos pointers
		if (self.get_next_pos()):
			pname = self.current_page
			page = self.buffer.get_page(pname)
			return page.get_element_from_page(self.current_pos)
		return None


	def close(self):
		# Closes the iterator
		self.current_page = None
		self.current_pos = None

	def get_attribute_types(self):
		# Returns a dictionary of attribute name: attribute type
		# E.g. if we have R(a int, b str), it will return {'a':'int','b':'str'}

		res = {}

		for i in range(self.numAttrib):
			res[self.attributes[i]] = self.types[i]

		return res

	def get_individual_values(self, tup):
		# When tup is a tuple of values read from disk it is a single string (e.g. '1 Hello 7')
		# when the relation has a signature R(a int, b text, c int), we want to get the individual values
		# this mathod takes a sting '1 Hello 7' for R(a int, b text, c int) and returns a dictionary:
		#	{'a':1, 'b':Hello, 'c':7}; as before, for simplicity strings can not have spaces
		# we assume that the values are well typed

		res = {}

		vals = tup.split(' ')
		for i in range(self.numAttrib):
			attrib = self.attributes[i]
			if (self.types[i] == 'int'):
				res[attrib] = int(vals[i])
			else:
				res[attrib] = vals[i]

		return res

	def insert_tuple(self, tup):
		# first run from first page, till the last one to check whether you have the tuple already
		# on the way make sure to find the first empty position

		# all is asked from the buffer

		# then just call insert_into_pos using the buffer
		# to save the changes also write the page!!!

		# If you come to the end, needs to create a new page and link it to the next one

		pass

# Test case:
'''
buff = Buffer()
R = Relation('R',['a','b'],['int','int'],buff)

R.insert_tuple('11 153') # New tuple
R.insert_tuple('27 1329') # Create a new next_page
R.insert_tuple('11 153') # Insert existing tuple
'''

