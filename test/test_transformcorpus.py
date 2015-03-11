import pytest


from corpusbuilder.Corpus import Corpus
from corpusbuilder.Extractor import Extractor as Extractor
from corpusbuilder.TransformCorpus import TransformCorpus as TransformCorpus

import datetime
import os
import shelve


class TestMerge:

	def setup(self):
	
		self.shelve_path = 'test/test_tmp/'

		self.extracted_merge = Extractor('test/test_sheets/test_letter_merge.xlsx', self.shelve_path + 'mergetest.shelve', 'PageID')
		self.extracted_merge.buildShelveFile('DT')

		self.TransformCorpus_merge = TransformCorpus(self.shelve_path + 'mergetest.shelve', test=True)

		self.extracted_strip = Extractor('test/test_sheets/test_letter_stripTags.xlsx', self.shelve_path + 'striptest.shelve', 'ID_COLUMN')
		self.extracted_strip.buildShelveFile()
		self.TransformCorpus_strip = TransformCorpus(self.shelve_path + 'striptest.shelve', test=True)
	
	def teardown(self):
		if os.path.isfile(self.shelve_path + 'mergetest_merge.shelve'):
			os.remove(self.shelve_path + 'mergetest_merge.shelve')
		if os.path.isfile(self.shelve_path + 'mergetest.shelve'):
			os.remove(self.shelve_path + 'mergetest.shelve')
		if os.path.isfile(self.shelve_path + 'striptest_strip.shelve'):
			os.remove(self.shelve_path + 'striptest_strip.shelve')
		if os.path.isfile(self.shelve_path + 'striptest.shelve'):
			os.remove(self.shelve_path + 'striptest.shelve')


	def test_merge(self):
		self.TransformCorpus_merge.merge('LetterID', 'merge_column')
		new_corpus = Corpus(self.shelve_path + 'mergetest_merge.shelve')
		assert list(new_corpus.__iter__()) == [{u'DT': 41583.50037037037, u'PageID': u'page_ID2', u'A_HEADER': u'a_value3', u'merge_column': u'MergePart1<pb/>MergePart2', u'LetterID': u'letterID'}]

	
	def test_tagStripper(self):
		simple_string = "Ok, this is a simple string. With a range! Of punctuation."
		assert self.TransformCorpus_strip.tagStripper(simple_string) == simple_string
		string_with_tag = "Ok, <this>this is a string</this>."
		assert self.TransformCorpus_strip.tagStripper(string_with_tag) == 'Ok, this is a string.'
		string_with_more_tags = '<thing="this_thing1">And <man>there</man> are many<thing/>'
		assert self.TransformCorpus_strip.tagStripper(string_with_more_tags) == 'And there are many'

	def test_stripTags(self):
		self.TransformCorpus_strip.stripTags('TEXT')
		strip_corpus = Corpus(self.shelve_path + 'striptest_stripTags.shelve')

		assert list(strip_corpus.__iter__()) == [{'ID_COLUMN': 'id1', 'TEXT': 'Ok, this is a simple string. With a range! Of punctuation.'},
																						 {'ID_COLUMN': 'id2', 'TEXT': 'Ok, this is a string.'},
																						 {'ID_COLUMN': 'id3', 'TEXT': 'And there are many'}
																						]

	def test_mergeByDateRange(self):
		# TEST THIS PROPERLY...!
		assert 1 == 1

	def test_dateRanges(self):
		self.TransformCorpus_daterange = TransformCorpus(self.shelve_path + 'dangerangetest.shelve', test=True)
		start_date = datetime.date(1991, 01, 01)
		end_date = datetime.date(1991, 01, 15)
		date_range = (start_date, end_date)
		interval = datetime.timedelta(days=30)
		interval_shift = datetime.timedelta(days=7)

		# FAILS... testing wrong date ranges...
		assert self.TransformCorpus_daterange.dateRanges(date_range, interval, interval_shift) == [(start_date,datetime.date(1991, 1, 8)),
																																								(datetime.date(1991, 1, 8), end_date)]
