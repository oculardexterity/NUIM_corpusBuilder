import pytest


from corpusbuilder.Corpus import Corpus
from corpusbuilder.Extractor import Extractor as Extractor
from corpusbuilder.TransformCorpus import TransformCorpus as TransformCorpus

import os
import shelve


class TestMerge:

	def setup(self):
	
		self.shelve_path = 'test/test_tmp/'

		self.extracted_merge = Extractor('test/test_sheets/test_letter_merge.xlsx', self.shelve_path + 'test.shelve', 'PageID')
		self.extracted_merge.buildShelveFile('DT')

		self.TransformCorpus_merge = TransformCorpus(self.shelve_path + 'test.shelve', test=True)

		#self.extracted_strip = Extractor() ## Do some stuff to this extractor
		#self.TransformCorpus_strip = TransformCorpus(self.shelve_path + 'strip_test.shelve', test=True)
	
	def teardown(self):
		if os.path.isfile(self.shelve_path + 'test_merge.shelve'):
				os.remove(self.shelve_path + 'test_merge.shelve')
		if os.path.isfile(self.shelve_path + 'test.shelve'):
				os.remove(self.shelve_path + 'test.shelve')
	

	def test_merge(self):
		self.TransformCorpus_merge.merge('LetterID', 'merge_column')
		new_corpus = Corpus(self.shelve_path + 'test_merge.shelve')
		assert list(new_corpus.__iter__()) == [{u'DT': 41583.50037037037, u'PageID': u'page_ID2', u'A_HEADER': u'a_value3', u'merge_column': u'MergePart1<pb/>MergePart2', u'LetterID': u'letterID'}]

	def test_strip_tags(self):
		assert 1 == 1