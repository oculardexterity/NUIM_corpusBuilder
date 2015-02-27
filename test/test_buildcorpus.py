import pytest

# Import modules for setup
import os
import shelve
import xlrd as xlrd

# Import module to test
import corpusbuilder.extractToShelve as extract

class TestBuildCorpus:

	def setup(self):
		self.test_simple_workbook = xlrd.open_workbook('test/test_sheets/test_simple.xlsx')
		self.test_simple_sheet = self.test_simple_workbook.sheet_by_index(0)
		
		self.test_id_clash_workbook = xlrd.open_workbook('test/test_sheets/test_id_clash.xlsx')
		self.test_id_clash_sheet = self.test_id_clash_workbook.sheet_by_index(0)
		self.id_column = 'ID'

		self.shelve_file_path = 'test/test_tmp/test.shelve'


	def test_getHeaders(self):
		assert extract.getHeaders(self.test_simple_sheet) == [u'A_HEADER', u'B_HEADER', u'ID']

	def test_getRowData(self):
		assert list(extract.getRowData(self.test_simple_sheet)) == [[u'a_value', u'b_value', u'id_1'],[u'a_value2', u'b_value2', u'id_2']]


	def test_buildRowDict(self):
		row = [u'a_value', u'b_value', u'id_1']
		headers = [u'A_HEADER', u'B_HEADER', u'ID']
		assert extract.buildRowDict(row, headers, self.id_column) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' }}
		# with the id_column value as the key

	def test_buildShelveFile_should_create_corpus_shelve_file(self):
		extract.buildShelveFile(self.shelve_file_path, self.test_simple_sheet, self.id_column) # call the function to be tested
		assert os.path.isfile(self.shelve_file_path) == True
		os.remove(self.shelve_file_path) 

	def test_buildShelveFile_should_write_properly(self):
		extract.buildShelveFile(self.shelve_file_path, self.test_simple_sheet, self.id_column) # call the function to be tested
		assert shelve.open(self.shelve_file_path) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' },
																							'id_2' : { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_2' }
																						}
		os.remove(self.shelve_file_path)

	def test_buildCorpusShelve_should_not_overwrite_existing_key(self):
		extract.buildShelveFile(self.shelve_file_path, self.test_id_clash_sheet, self.id_column) # builds pickle
		assert shelve.open(self.shelve_file_path) != { 'id_1' : { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_1' } }
		os.remove(self.shelve_file_path)
		#IF, given two things with the same id, check the timestamp column...

		#DO THIS NEXT... {have to edit Excel file to add a duplicate}
		# OR ADD A NEXT EXCEL FILE?? Probably. Move test file to inside test directory?
		# same with tmp >> test/tmp

		# also... see how long it will take with a big file...!
	

	