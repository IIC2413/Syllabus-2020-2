'''
Everything in this activity is a vast simplification of how a database is actually implemented
If you want to learn how these things are done for real, take the Database Implementation course

Here we implement the pages that guard our data

We do this in the class Page

The page object contains one data page that is stored on the disk
The structure of the page we support is the following:

	1. Page has a name pname, which for us is a file on the disk
	2. The following five lines are 5 tuples of some relation that we guard on this page (here we simplify a lot),
		or a string <EMPTY>, if we do not have a tuple here
	3. The final line is the name of the next page in our relation in the format <NEXT> next_page
		if there is no next page this next_page = '<NULL>'

Some examples of pages for a relation R(a int, b text)

p1 (this is the name of the file on the disk):
####################
##1 Hello          #
##2 World		   #
##<EMPTY>		   #
##<EMPTY>		   #
##3 Not_this_again!#
##<NEXT> p2		   #
####################

p2:
####################
##1 Some data      #
##<EMPTY>		   #
##<EMPTY>		   #
##<EMPTY>		   #
##7 			   #
##<NEXT> <NULL>	   #
####################

This corresponds to an instance of R that has tuples

 R:
 a | b
 --------------------
 1 | Hello
 2 | World
 3 | Not this again!
 1 | Some data
 7 |

Note that this could fit on a single page, but database systems often leave some space on pages guarding their data
so that they can write more tuples without having to assign disk space again (by creating a new page)

Anyway, the Page class will allow us to guard pages in memory, and flush them onto disk

'''

class Page:

	# The constructor creates a completely empty page with name pname
	def __init__(self, pname, size = 5):
		self.size = size
		self.pname = pname
		self.data = ['<EMPTY>'] * size
		self.next = '<NULL>'
		self.dirty = False # A bit that tells us if we made any changes to the page

	# This operator will write the page to disk
	# It rewrites the existing content of the page, so be careful
	def write_page(self):
		if not(self.dirty):
			print('No need to write the page')
			return

		else:
			diskPage = open(self.pname, 'w', encoding='utf-8')
			for i in range(self.size):
				diskPage.write(self.data[i] + '\n')
			diskPage.write('<NEXT> ' + self.next)
			diskPage.close()
			# We also reset the dirty bit
			self.dirty = False

	# If the page already exists on the disk, we can read its data into memory
	def read_from_disk(self):

		diskPage = open(self.pname, 'r', encoding='utf-8')

		# Need to deal with this
		if not(diskPage):
			print('Non existing page')

		lines = diskPage.readlines()
		diskPage.close()

		lines = list(map(lambda x: x.strip(), lines))

		for i in range(self.size):
			self.data[i] = lines[i]

		self.next = lines[self.size][len('<NEXT> '):]


	# Allows to set the next page
	def set_next_page(self, next_pname):
		self.next = next_pname
		self.dirty = True

	# Allows to fetch the name of the next page
	# Returns None is there is no next page
	def get_next_page_name(self):
		if self.next == '<NULL>':
			return None
		return self.next

	# Tells us if there is empty space on the page -- not important for us
	def has_empty(self):

		for i in range(self.size):
			if self.data[i] == '<EMPTY>':
				return i

		return -1

	def insert_into_pos(self, pos, value):
		'''
		Inserta en la página pname, en el casillero pos el string con valor value.
		Si se ingresa una posición no válida la función no hace nada
		'''
		if pos > self.size - 1:
			print('Position not valid')
			return

		if '<EMPTY>' not in self.data[pos]:
			print('Position not empty')
			return

		self.data[pos] = value

		# We changed the page, so it's dirty
		self.dirty = True


	def delete_from_pos(self, pos):
		'''
		Setea el valor <EMPTY> en la posición indicada.
		'''
		
		if pos >= self.size - 1:
			print('Position not valid')
			return

		if '<EMPTY>' in self.data[pos]:
			print('Position already empty')
			return

		self.data[pos] = '<EMPTY>'

		# We changed the page, so it's dirty
		self.dirty = True


	def get_element_from_page(self, pos):

		if pos > self.size -1:
			print('Position not valid')
			return

		return self.data[pos]

