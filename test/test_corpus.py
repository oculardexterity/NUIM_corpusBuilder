import pytest
import xlrd

# module to test
from corpusbuilder.corpus import Corpus


class TestCorpus:

	def setup(self):
		self.corpus = Corpus()

	def test_something(self):
		thing = self.corpus.something()
		assert thing == 'something'
		assert type(thing) == type('string')
