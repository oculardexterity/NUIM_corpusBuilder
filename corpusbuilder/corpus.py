import shelve
import extractToShelve as extract


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



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
		return CorpusObject(self.shelve_file[k])

	def __len__(self):
		return len(self.shelve_file)




class CorpusObject(Bunch):
	def __init__(self, item):
		super(CorpusObject, self).__init__(**item)
	
	def text(self):
		try:
			return self.Translation
		except AttributeError:
			raise AttributeError("This corpus does not have a text property")





if __name__ == '__main__':
	corpus = Corpus('corpus/corpus.shelve')

	for item in corpus:
		if len(item.text()) < 50:
		#if item.Letter == 200:
			print bcolors.HEADER + '----' + str(item.DATE_created) + '----' + str(item.Letter) + bcolors.ENDC
			print item.text()

	print '................................\n', len(corpus)