
from Corpus import Corpus as Corpus

import datetime
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
		""" 
		stripTags function builds new corpus file with one field stripped
		Inputs:
			column_to_strip: the column to remove tags from
		"""
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

	def mergeByDateRange(self, date_column, date_range, interval):
		""""""
		self.before_transform('mergeByDateRange')

		old_shelve = shelve.open(self.old_shelve_path)
		new_shelve = shelve.open(self.new_shelve_path)


		for daterange in self.dateRanges(date_range, interval):
			dr_string = str(daterange[0]) + '---' + str(daterange[1])
			new_shelve[dr_string] = {'DateRange': dr_string, 'Translation': "" }

			for key, row in old_shelve.items():
				#print row[date_column]
				try:
					current_row_date = datetime.datetime.strptime(row[date_column], '%Y-%m-%d').date()
					if daterange[0] <= current_row_date < daterange[1]:
						#print daterange[0], daterange[1]
						#print row['Translation']
						updated_row = {'DateRange': dr_string, 'Translation': new_shelve[dr_string]['Translation'] + row['Translation']}
						new_shelve[dr_string] = updated_row
				except:
					pass
				
					
				

					


		print new_shelve 


		



	def dateRanges(self, dRange, interval):
		start_date = dRange[0]
		end_date = dRange[1]

		date_range_list = []

		working_date = start_date

		while working_date < end_date:
			next_working_date = working_date + datetime.timedelta(days=7)
			new_range = (working_date, next_working_date)
			date_range_list.append(new_range)
			working_date = next_working_date

		return date_range_list

	












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
	transform = TransformCorpus('corpus/corpus_merge_stripTags.shelve')
	

	start_date = datetime.date(1915, 11, 01)
	end_date = datetime.date(1916, 10, 31)
	date_range = (start_date, end_date)
	interval = datetime.timedelta(days=7)
	transform.mergeByDateRange('DATE_created', date_range, interval)

if __name__ == "__main__":
	main()