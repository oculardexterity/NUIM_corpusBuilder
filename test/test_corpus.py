import os
import pytest
import shelve
import xlrd

# module to test
from corpusbuilder.Corpus import Corpus
from corpusbuilder import Extractor as extract

class TestCorpus:

	def setup(self):

		# build corpus shelve...
		self.id_column = 'ID'
		self.shelve_path = 'test/test_tmp/test.shelve'

		self.extractSimple = self.extractSimple = extract.Extractor('test/test_sheets/test_simple.xlsx', self.shelve_path, self.id_column)
		self.extractSimple.buildShelveFile(test=True)

		# Init
		self.corpus = Corpus(self.shelve_path)

	def teardown(self):
		os.remove(self.shelve_path)


	def test_corpus_iter(self):
		#print list(self.corpus.__iter__())
		assert list(self.corpus.__iter__()) == [{u'A_HEADER': u'a_value', u'ID': u'id_1', u'B_HEADER': u'b_value'}, {u'A_HEADER': u'a_value2', u'ID': u'id_2', u'B_HEADER': u'b_value2'}]

	def test_corpus_getitem(self):
		assert self.corpus['id_1'].A_HEADER == u'a_value'

	def test_corpus_len(self):
		assert len(self.corpus) == 2

	def test_corpusObject_dot_notation(self):
		assert list(self.corpus.__iter__())[0].A_HEADER == u'a_value'

	def test_corpusObject_text_function_no_text(self):
		with pytest.raises(AttributeError) as err:
			list(self.corpus.__iter__())[0].text()
		assert err.value.message == "This corpus does not have a text property"

	def test_corpusObject_text_function_with_text(self):
		assert 1 == 1
