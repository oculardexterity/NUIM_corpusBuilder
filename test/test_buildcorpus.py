import pytest

# Import modules for setup
import os
import shelve
import xlrd as xlrd

# Import module to test
import corpusbuilder.buildcorpus as cb

class TestBuildCorpus:

	def setup(self):
		workbook = xlrd.open_workbook('test.xlsx')
		self.sheet = workbook.sheet_by_index(0)
		self.id_column = 'ID'


	def test_getHeaders(self):
		assert cb.getHeaders(self.sheet) == [u'A_HEADER', u'B_HEADER', u'ID']

	def test_getRowData(self):
		assert list(cb.getRowData(self.sheet)) == [[u'a_value', u'b_value', u'id_1'],[u'a_value2', u'b_value2', u'id_2']]


	def test_buildRowDict(self):
		row = [u'a_value', u'b_value', u'id_1']
		headers = [u'A_HEADER', u'B_HEADER', u'ID']
		assert cb.buildRowDict(row, headers, self.id_column) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' }}
		# with the id_column value as the key

	def test_buildCorpusShelve(self):
		# build shelf file
		shelve_file_path = 'tmp/test.shelve'
		cb.buildShelfFile(shelve_file_path, self.sheet, self.id_column) # call the function to be tested
		assert os.path.isfile(shelve_file_path) == True 
		assert shelve.open(shelve_file_path) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' },
																							'id_2' : { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_2' }
																						}
		os.remove(shelve_file_path)

	def test_buildCorpusShelveRemovesDuplicatePages(self):
		assert 1 == 1
		#DO THIS NEXT... {have to edit Excel file to add a duplicate}
		# OR ADD A NEXT EXCEL FILE?? Probably. Move test file to inside test directory?
		# same with tmp >> test/tmp

		# also... see how long it will take with a big file...!
	

	