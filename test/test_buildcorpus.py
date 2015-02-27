import pytest

# Import modules for setup
import os
import shelve
import xlrd as xlrd

# Import module to test
import corpusbuilder.extractToShelve as extract

class TestBuildCorpus:

	def setup(self):
		workbook = xlrd.open_workbook('test/test_sheets/test_simple.xlsx')
		self.sheet = workbook.sheet_by_index(0)
		self.id_column = 'ID'


	def test_getHeaders(self):
		assert extract.getHeaders(self.sheet) == [u'A_HEADER', u'B_HEADER', u'ID']

	def test_getRowData(self):
		assert list(extract.getRowData(self.sheet)) == [[u'a_value', u'b_value', u'id_1'],[u'a_value2', u'b_value2', u'id_2']]


	def test_buildRowDict(self):
		row = [u'a_value', u'b_value', u'id_1']
		headers = [u'A_HEADER', u'B_HEADER', u'ID']
		assert extract.buildRowDict(row, headers, self.id_column) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' }}
		# with the id_column value as the key

	def test_buildShelveFile_should_create_corpus_shelve_file(self):
			# build shelf file
		shelve_file_path = 'test/test_tmp/test.shelve'
		extract.buildShelveFile(shelve_file_path, self.sheet, self.id_column) # call the function to be tested
		assert os.path.isfile(shelve_file_path) == True
		os.remove(shelve_file_path) 

	def test_buildShelveFile_should_write_properly(self):
		# build shelf file
		shelve_file_path = 'test/test_tmp/test.shelve'
		extract.buildShelveFile(shelve_file_path, self.sheet, self.id_column) # call the function to be tested
		assert shelve.open(shelve_file_path) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' },
																							'id_2' : { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_2' }
																						}
		# remove test shelf
		os.remove(shelve_file_path)

	def test_buildCorpusShelve_should_remove_duplicate_pages(self):
		assert 1 == 1
		#IF, given two things with the same id, check the timestamp column...

		#DO THIS NEXT... {have to edit Excel file to add a duplicate}
		# OR ADD A NEXT EXCEL FILE?? Probably. Move test file to inside test directory?
		# same with tmp >> test/tmp

		# also... see how long it will take with a big file...!
	

	