import shelve
import xlrd as xlrd

#MOVE THESE TO MAIN!!
workbook = xlrd.open_workbook('corpus/1916letters_all_translations12012015.xlsx')
sheet = workbook.sheet_by_index(0)
shelveFile = 'corpus/corpus.shelve'
id_column = 'Page'

def getHeaders(sheet):
	headers = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
	return headers

def getRowData(sheet):
	rows = []
	for i in range(1,sheet.nrows):
		row = [sheet.cell(i, col_index).value for col_index in range(sheet.ncols)]
		# Generator yields row at a time ...
		yield row

def buildRowDict(row, headers, id_column):
	# this line here... no need to do this every time?
	id_index = headers.index(id_column)

	row_id = str(row[id_index])
	row_dict = { row_id: {} }
	for i, cell in enumerate(row):
		row_dict[row_id][headers[i]] = cell
	return row_dict


# MAIN FUNCTION OF THE SHOW....
def buildShelveFile(shelf_file_path, sheet, id_column, conflict_res_column=0, test=False): #and conflict_res_order
	shelve_file = shelve.open(shelf_file_path)
	headers = getHeaders(sheet)
	resolveConflict = chooseBetween

	for row in getRowData(sheet):
		row = buildRowDict(row, headers, id_column)
		
		# HERE SET FUNCTION TO RESOLVE CONFLICT ... function should return item to overwrite
		
		
		if str(row.keys()[0]).encode('ascii') in shelve_file:
			if not test: # Prevents the chooseBetween function from working to test should_not_overwrite_existing
				#shelve_file[row.keys()[0]] = resolveConflict(shelve_file[row.keys()[0]], row[row.keys()[0]], conflict_res_column)
				resolveConflict(shelve_file[row.keys()[0]], row[row.keys()[0]], conflict_res_column)
		else:
			# Just write
			shelve_file[row.keys()[0]] = row[row.keys()[0]]

		## fields to farm out to other file, plus filelocation??
	shelve_file.close()


def chooseBetween(shelf_row, new_row, column_to_compare, select='greater'):
	if shelf_row[column_to_compare] < new_row[column_to_compare] and select == 'greater':
		return new_row
	elif shelf_row[column_to_compare] < new_row[column_to_compare] and select == 'lesser':
		return shelf_row


def main():
	buildShelveFile(shelveFile, sheet, id_column, 'Translation_Timestamp')


if __name__ == "__main__":
	main()

