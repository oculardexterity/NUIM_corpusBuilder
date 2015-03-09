
from Corpus import Corpus as Corpus
import shelve
import os

class Merge():

	def __init__(self, old_shelve_path, new_id, merge_column, new_shelve_path):
		self.old_shelve_path = old_shelve_path
		self.new_shelve_path = new_shelve_path
		self.merge_column = merge_column
		self.new_id = new_id
	



	def merge(self):
		if os.path.isfile(self.new_shelve_path):
				os.remove(self.new_shelve_path)
	
		old_shelve = shelve.open(self.old_shelve_path)
		new_shelve = shelve.open(self.new_shelve_path)

		for key, row in sorted(old_shelve.items()):

			current_row_key = str(row[self.new_id]).encode('ascii')
			#print 'CRK: ' +  current_row_key

			if current_row_key in new_shelve:
				print 'yes'

			 
				row[self.merge_column] = new_shelve[current_row_key][self.merge_column] + '--------------' + row[self.merge_column]
				new_shelve[current_row_key] = row
			else:
				print 'no'
				new_shelve[current_row_key] = row
			
			print new_shelve

def main():
	merge = Merge('test/test_tmp/test.shelve', 'LetterID', 'merge_column', 'test/test_tmp/new_test.shelve')
	merge.merge()

if __name__ == "__main__":
	main()