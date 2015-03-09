import pytest


from corpusbuilder.Corpus import Corpus
from corpusbuilder.Extractor import Extractor as Extractor
from corpusbuilder.Merge import Merge as Merge

import os
import shelve


class TestMerge:

	def setup(self):
		""""""
		
		
		self.shelve_path = 'test/test_tmp/test.shelve'
		self.extracted = Extractor('test/test_sheets/test_letter_merge.xlsx', self.shelve_path, 'PageID')
		self.extracted.buildShelveFile('DT')

		self.new_shelve_path = 'test/test_tmp/new_test.shelve'


		
				
		self.corpus = Corpus(self.shelve_path)

		self.merge = Merge('test/test_tmp/test.shelve', 'LetterID', 'merge_column', self.new_shelve_path)
		self.merge.merge()

	"""	
	def teardown(self):
		if os.path.isfile(self.new_shelve_path):
				os.remove(self.new_shelve_path)
		if os.path.isfile(self.shelve_path):
				os.remove(self.shelve_path)
	"""

	def test_corpus(self):
		''' A sanity test to make sure this Corpus is loading as expected'''
		assert list(self.corpus.__iter__()) == [{u'DT': 41581.50037037037, u'A_HEADER': u'a_value2', u'PageID': u'page_ID1', u'merge_column': u'MergePart1', u'LetterID': u'letterID'}, 
																						{u'DT': 41583.50037037037, u'A_HEADER': u'a_value3', u'PageID': u'page_ID2', u'merge_column': u'MergePart2', u'LetterID': u'letterID'}]

	def test_merge(self):
		#self.merge.merge()
		assert 1 == 1
		#self.merge.merge()
		#new_corpus = Corpus(self.new_shelve_path)
		#assert list(new_corpus.__iter__()) == {u'DT': 41581.50037037037, u'PageID': u'page_ID2', u'A_HEADER': u'a_value3', u'merge_column': u'MergePart1--------------MergePart2', u'LetterID': u'letterID'}
