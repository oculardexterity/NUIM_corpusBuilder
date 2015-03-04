import pytest

# Import modules for setup
import os
import shelve
import xlrd as xlrd

# Import module to test
import corpusbuilder.Extractor as extract

class TestBuildCorpus:

	def setup(self):
		self.id_column = 'ID'

		self.shelve_path = 'test/test_tmp/test.shelve'

		self.extractSimple = extract.Extractor('test/test_sheets/test_simple.xlsx', self.shelve_path, self.id_column)
		self.extractClash = extract.Extractor('test/test_sheets/test_id_clash.xlsx', self.shelve_path, self.id_column)
		self.extractDatetime = extract.Extractor('test/test_sheets/test_datetime.xlsx', self.shelve_path, self.id_column)


	def teardown(self):
		if os.path.isfile(self.shelve_path):
			os.remove(self.shelve_path) 

	def test_getHeaders(self):
		assert self.extractSimple.getHeaders() == ['A_HEADER', 'B_HEADER', u'ID']

	def test_getRowData(self):
		assert list(self.extractSimple.getRowData()) == [[u'a_value', u'b_value', u'id_1'],[u'a_value2', u'b_value2', u'id_2']]


	def test_buildRowDict(self):
		row = [u'a_value', u'b_value', u'id_1']
		print self.extractSimple.buildRowDict(row)
		assert self.extractSimple.buildRowDict(row) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' }}
		# with the id_column value as the key

	def test_buildShelveFile_should_create_corpus_shelve_file(self):
		self.extractSimple.buildShelveFile() # call the function to be tested
		assert os.path.isfile(self.shelve_path) == True
		os.remove(self.shelve_path) 

	def test_buildShelveFile_should_write_properly(self):
		self.extractSimple.buildShelveFile() # call the function to be tested
		assert shelve.open(self.shelve_path) == { 'id_1' : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' },
																							'id_2' : { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_2' }
																						}
		os.remove(self.shelve_path)

	def test_buildCorpusShelve_should_not_overwrite_existing_key(self):
		self.extractClash.buildShelveFile(test=True) # builds pickle
		assert shelve.open(self.shelve_path) != { u'id_1' : { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_1' } }
		os.remove(self.shelve_path)

	
	def test_buildCorpusShelve_should_overwrite_if_duplicate(self):
		self.extractDatetime.buildShelveFile('DT', test=False)
		assert shelve.open(self.shelve_path) == { 'id_1' : { u'DT' : 41581.50037037037, u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_1' }  }
		os.remove(self.shelve_path)

	def test_chooseBetween_should_choose_correct(self):
		shelve_file_row =  { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value', u'ID': u'id_1' } 
		row = 						 { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2', u'ID': u'id_1' } 
		assert self.extractSimple.chooseBetween(shelve_file_row, row, 'A_HEADER') == row

	def test_chooseBetween_with_datetime_should_choose_correct(self):
		shelve_file_row =  { u'DT' : 41547.59240740741, u'B_HEADER': u'b_value', u'ID': u'id_1' } 
		row = 						{ u'DT' : 41581.50037037037, u'B_HEADER': u'b_value2', u'ID': u'id_1' } 
		assert self.extractSimple.chooseBetween(shelve_file_row, row, 'DT') == row




