import pytest

# Import modules for setup
import xlrd as xlrd

# Import module to test
import corpusbuilder.buildcorpus as cb

class TestBuildCorpus:

	def setup(self):
		workbook = xlrd.open_workbook('test.xlsx')
		self.sheet = workbook.sheet_by_index(0)

	def test_getHeaders(self):
		assert cb.getHeaders(self.sheet) == [u'A_HEADER', u'B_HEADER']

	def test_getRowData(self):
		assert cb.getRowData(self.sheet) == [[u'a_value', u'b_value'],[u'a_value2', u'b_value2']]

	def test_getDataDict(self):
		assert cb.getDataDict(self.sheet) == { 0 : { u'A_HEADER' : u'a_value', u'B_HEADER': u'b_value' },
																					 1 : { u'A_HEADER' : u'a_value2', u'B_HEADER': u'b_value2' },
																				}

		

	

	