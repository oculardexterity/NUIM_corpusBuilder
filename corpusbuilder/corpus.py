import shelve
import extractToShelve as extract

class Bunch(dict):
	def __init__(self, **kw):
		dict.__init__(self, kw)
		self.__dict__ = self

	def __getstate__(self):
		return self

	def __setstate__(self, state):
		self.update(state)
		self.__dict__ = self


class Corpus():
	def __init__(self, shelve_file_path):
		self.shelve_file = shelve.open(shelve_file_path)

	def __iter__(self):
		for key, value in sorted(self.shelve_file.items()):
			yield CorpusObject(value)

	def __getitem__(self, k):
		return k

	def __len__(self):
		return len(self.shelve_file)

class CorpusObject(Bunch):
	def __init__(self, item):
		super(CorpusObject, self).__init__(**item)
	
	def text(self):
		return self.Translation

if __name__ == '__main__':
	corpus = Corpus('corpus/corpus.shelve')

	for item in corpus:
		#if item.Letter == 200:
		print '----' + str(item.Page) + '----' + str(item.Letter)
		print item.text()

	print '................................\n', len(corpus)