import pytest


from corpusbuilder.Corpus import Corpus
from corpusbuilder.Extractor import Extractor as Extractor
from corpusbuilder.FixCorpus import FixCorpus as FixCorpus

import os
import shelve


class TestMerge:

	def setup(self):
	
		self.shelve_path = 'test/test_tmp/test.shelve'

		self.extracted = Extractor('test/test_sheets/test_letter_merge.xlsx', self.shelve_path, 'PageID')
		self.extracted.buildShelveFile('DT')

		self.new_shelve_path = 'test/test_tmp/new_test.shelve'

		self.fixCorpus = FixCorpus(self.shelve_path, 'LetterID', 'merge_column', self.new_shelve_path)

	
	
	def teardown(self):
		if os.path.isfile(self.new_shelve_path):
				os.remove(self.new_shelve_path)
		if os.path.isfile(self.shelve_path):
				os.remove(self.shelve_path)
	

	def test_merge(self):
		self.fixCorpus.merge()
		new_corpus = Corpus(self.new_shelve_path)
		assert list(new_corpus.__iter__()) == [{u'DT': 41583.50037037037, u'PageID': u'page_ID2', u'A_HEADER': u'a_value3', u'merge_column': u'MergePart1--------------MergePart2', u'LetterID': u'letterID'}]