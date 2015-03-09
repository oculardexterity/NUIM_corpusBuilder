import os
import shelve
import xlrd as xlrd


class Extractor:
	def __init__(self, sheet_path, shelve_path, id_column):
		self.sheet = xlrd.open_workbook(sheet_path).sheet_by_index(0)
		self.shelve_path = shelve_path
		self.id_column = id_column
		self.headers = self.getHeaders()

	def getHeaders(self):
		headers = [self.sheet.cell(0, col_index).value for col_index in range(self.sheet.ncols)]
		return headers

	def getRowData(self):
		rows = []
		for i in range(1,self.sheet.nrows):
			row = [self.sheet.cell(i, col_index).value for col_index in range(self.sheet.ncols)]
			# Generator yields row at a time ...
			yield row

	def buildRowDict(self, row): #row, headers, id_column):
		id_index = self.headers.index(self.id_column)
		row_id = str(row[id_index])
		row_dict = { row_id: {} }
		for i, cell in enumerate(row):
			row_dict[row_id][self.headers[i]] = cell
		return row_dict



	# MAIN FUNCTION OF THE SHOW....
	def buildShelveFile(self, conflict_res_column=False, test=False):
		# Kills old shelve files if existing
		if os.path.isfile(self.shelve_path):
				os.remove(self.shelve_path)

		shelve_file = shelve.open(self.shelve_path)


		for row in self.getRowData():
			row = self.buildRowDict(row)

			current_row_key = str(row.keys()[0].encode('ascii'))

			if current_row_key in shelve_file:
				if not test: # Prevents the chooseBetween function from working to test should_not_overwrite_existing

					row_to_write = self.chooseBetween(shelve_file[current_row_key], row[current_row_key], conflict_res_column)
					shelve_file[current_row_key] = row_to_write
			else:
				shelve_file[current_row_key] = row[current_row_key]


	def chooseBetween(self, shelf_row, new_row, column_to_compare):
		""" Fix this for all options """
		if shelf_row[column_to_compare] < new_row[column_to_compare]:
			return new_row
		else:
			return shelf_row


def main():
	sheet_path = 'corpus/1916letters_all_translations12012015.xlsx'
	shelve_path = 'corpus/corpus.shelve'
	id_column = 'Page'

	extractor = Extractor(sheet_path, shelve_path, id_column)
	extractor.buildShelveFile('Translation_Timestamp')


if __name__ == "__main__":
	main()

