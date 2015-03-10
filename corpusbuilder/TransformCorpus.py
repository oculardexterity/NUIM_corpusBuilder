
from Corpus import Corpus as Corpus

import os
import re
import shelve

class TransformCorpus():

	def __init__(self, old_shelve_path, new_shelve_path = "", test = False):
		self.old_shelve_path = old_shelve_path
		self.new_shelve_path = new_shelve_path
		self.test = test
		
		self.CLEANING_PATTERN = [("no-group", "<unclear>questionable reading</unclear>"), # appeared in letter 1004 several times
                    ("no-group", "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=\.,-]+-->"),
                    #("no-group", "[\d\.]+[ap]m"), #remove times e.g. 5pm or 4.30pm
                    #("no-group", "\'s"), #remove Gen. 's' e.g. Paul's
                    #("no-group", "[\d/'\.]+"),
                    #("no-group", "\s(\w\.)+\s"),
                    #("no-group", "&[#\w\d]+;"), 
                    #("use-group", "[\W]*(\w+[\w\'-/\.]*\w+|\w|&)[\W]*")
                     ] # 1916 letter cleaning pattern


	def merge(self, new_id, merge_column, break_string = "<pb/>"):
		""" 
		Merge function builds new corpus file with one merged field.
		Inputs:
			new_id: column in existing shelve to use as the new ID (e.g. Letter ID)
			merge_column: column to be merged (e.g. the Letter text of multiple pages)
			break_string: string for marking the join on merge (e.g. a <pb/> tag)
		"""

		# Builds new file path if none, then asks OK to overwrite if exists
		self.before_transform('merge')

		# Opens old and new shelve files
		old_shelve = shelve.open(self.old_shelve_path)
		new_shelve = shelve.open(self.new_shelve_path)

		for key, row in sorted(old_shelve.items()):
			current_row_key = str(row[new_id]).encode('ascii')
			#print 'CRK: ' +  current_row_key
			if current_row_key in new_shelve:	 
				row[merge_column] = new_shelve[current_row_key][merge_column] + break_string + row[merge_column]
				new_shelve[current_row_key] = row
			else:
				new_shelve[current_row_key] = row



	def stripTags(self, column_to_strip):
		self.before_transform('stripTags')

		old_shelve = shelve.open(self.old_shelve_path)
		new_shelve = shelve.open(self.new_shelve_path)

		for key, row in sorted(old_shelve.items()):
			row[column_to_strip] = self.tagStripper(row[column_to_strip])
			new_shelve[key] = row
	
	def tagStripper(self, strg):
		# By gods, complex... work out how this works later
		for typeOf, pat in self.CLEANING_PATTERN:
			if typeOf == "no-group":
				strg = "".join(re.split(pat , strg))
			elif typeOf == "use-group":
				regex = re.compile(pat)
				lst = []
				for item in strg.split():
					mm = regex.match(item)
					if mm:
						lst.append(mm.group(1))
				strg = "".join(lst)
		return strg




	












	def before_transform(self, transform_name):
		# Determines new shelve file. If unspecified, use old with _merge appended
		if self.new_shelve_path == "":
			self.new_shelve_path = self.old_shelve_path.split(".")[0] + '_' + transform_name + '.shelve'
		print self.test

		# Checks whether test is True, then whether input allows overwrite if working 
		if not self.test:	
			if self.prevent_overwrite(self.new_shelve_path):
				raise Exception('Merge halted to prevent overwrite')
				raise SystemExit


	def prevent_overwrite(self, the_file):
		if os.path.isfile(the_file):
			if raw_input("Overwrite existing corpus? 'y' to confirm: ") == 'y':
				print 'answered ok to overwrite'
				os.remove(the_file)
				return False
			else:
				return True
		else:
			return False
			

def main():
	transform = TransformCorpus('corpus/corpus_merge.shelve')
	transform.stripTags('Translation')

if __name__ == "__main__":
	main()