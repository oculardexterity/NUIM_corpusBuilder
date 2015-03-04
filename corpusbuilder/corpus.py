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
	def __init__(self, shelve_path, text_key):
		self.shelve_file = shelve.open(shelve_path)

	def __iter__(self):
		for key, value in sorted(self.shelve_file.items()):
			yield CorpusObject(value)

	def __getitem__(self, k):
		return CorpusObject(self.shelve_file[k])

	def __len__(self):
		return len(self.shelve_file)

class CorpusObject(Bunch):
	def __init__(self, item):
		super(CorpusObject, self).__init__(**item)
	
	def text(self):
		try:
			return self.text_key
		except AttributeError:
			raise AttributeError("This corpus does not have a text property")





if __name__ == '__main__':
	corpus = Corpus('corpus/corpus.shelve')

	for item in corpus:
		#if item.Letter == 200:
		print '----' + str(item.Page) + '----' + str(item.Letter)
		print item.text()

	print '................................\n', len(corpus)