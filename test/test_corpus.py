import os
import pytest
import shelve
import xlrd

# module to test
from corpusbuilder.corpus import Corpus
from corpusbuilder import extractToShelve as extract

class TestCorpus:

	def setup(self):

		# build corpus shelve...
		self.test_simple_workbook = xlrd.open_workbook('test/test_sheets/test_simple.xlsx')
		self.test_simple_sheet = self.test_simple_workbook.sheet_by_index(0)
		self.id_column = 'ID'
		self.shelve_file_path = 'test/test_tmp/test.shelve'
		extract.buildShelveFile(self.shelve_file_path, self.test_simple_sheet, self.id_column, test=True)

		# Ini
		self.corpus = Corpus(self.shelve_file_path)

	def teardown(self):
		os.remove(self.shelve_file_path)


	def test_corpus_iter(self):
		#print list(self.corpus.__iter__())
		assert list(self.corpus.__iter__()) == [{u'A_HEADER': u'a_value', u'ID': u'id_1', u'B_HEADER': u'b_value'}, {u'A_HEADER': u'a_value2', u'ID': u'id_2', u'B_HEADER': u'b_value2'}]


	def test_corpusObject_dot_notation(self):
		assert list(self.corpus.__iter__())[0].A_HEADER == u'a_value'