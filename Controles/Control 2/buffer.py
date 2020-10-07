from pageNew import *

import os


class Buffer:

	# The constructor initializes the buffer
	def __init__(self, size = 4):
		self.buffSize = size # Size of our buffer; set super low so that swapping occurrs
		self.frames = [None] * self.buffSize # The array that has the pages -- i.e. the buffer frames
		self.pages_dict = {} # The disctionary that maps page name to a frame -- e.g. {'p1': 1}
		self.occupied = 0 # How many buffer frames are occupied currently
		self.clock_pos = 0 # The current clock position

	# Tells us if the buffer is full
	def isFull(self):
		if self.buffSize == self.occupied:
			return True
		return False

	# Loads a page 'pname' from disk, and puts it into an available frame
	def fetch_page(self, pname):

		# Is the page already in the buffer?
		if pname in self.pages_dict.keys():
			print('You already have it')
			return
		
		if self.isFull():
			# print('The buffer is full')
			to_evict = self.frames[self.clock_pos].pname
			self.evict_page(to_evict)
			#return

		# Get the content of pname from the disk
		newPage = Page(pname)
		newPage.read_from_disk()

		# Insert into frames; we made space above
		self.frames[self.clock_pos] = newPage

		# Insert the page name into the dictionary to be able to look for it in the Buffer
		self.pages_dict[pname] = self.clock_pos

		# Update the clock and occupancy
		self.clock_pos = (self.clock_pos + 1) % self.buffSize
		self.occupied = self.occupied + 1


	def create_page(self, pname):
		# Creates a new page, writes it onto disk, and loads it into the buffer
		# Also returns the created page

		if not(os.path.isfile('./' + pname)):
			page = Page(pname)
			page.dirty = True
			page.write_page()
			self.fetch_page(pname)

		return self.get_page(pname)



	def fetch_into_frame(self,pname,frame):
		# Fetches the page pname into the frame self.frames[frame]

		# Is the page already in the buffer?
		if pname in self.pages_dict.keys():
			print('You already have it')
			return

		if not(frame in range(self.buffSize)):
			print('Non existing frame')
			return

		# To fetch into this frame we reset the clock
		self.clock_pos = frame
		self.fetch_page(pname)



	# Loads a page 'pname' from disk, and puts it into an available frame
	def evict_page(self, pname):

		#print('Evicting')

		# Is the page already in the buffer?
		if not(pname in self.pages_dict.keys()):
			print('Page not in the buffer')
			return

		frame = self.pages_dict[pname]

		if (self.frames[frame] is None):
			return

		# If the page is dirty (i.e. it chaged), we write it to disk
		if self.frames[frame].dirty:
			# This is a Page object, so we write it to disk
			self.frames[frame].write_page()
		
		# Insert into frames; we made space above
		self.frames[frame] = None

		# Remove the entry from the dictionary
		del self.pages_dict[pname]

		# Update the clock and occupancy
		# Clock stays the same
		#self.clock_pos = (self.clock_pos - 1) % self.buffSize
		self.occupied = self.occupied - 1

	def flush_buffer(self):
		# This method empties the buffer

		# First we get the "live" pages
		keys = []
		for key in self.pages_dict.keys():
			keys.append(key)

		# NExt we evict all those pages
		for key in keys:
			self.evict_page(key)

		self.clock_pos = 0

	# Returns us a page with pname to work with
	def get_page(self, pname):
		# If the page is not in the buffer, fetch it
		if not(pname in self.pages_dict.keys()):
			self.fetch_page(pname)

		return self.frames[self.pages_dict[pname]]

	def flush_and_fill(self,pname,num):
		# Empties the buffer, and loads num pages starting from pname if there are as many

		# Flush the buffer
		self.flush_buffer()

		currentPage = pname

		# Get the starting page
		self.fetch_page(currentPage)

		for i in range(num-1):
			nextPage = self.frames[self.pages_dict[currentPage]].next
			if nextPage == '<NULL>':
				return currentPage
			else:
				self.fetch_page(nextPage)
				currentPage = nextPage

		# Returns the name of the last page loaded
		return currentPage


