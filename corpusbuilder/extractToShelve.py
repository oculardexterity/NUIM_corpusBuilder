import shelve
import xlrd as xlrd

#MOVE THESE TO MAIN!!
workbook = xlrd.open_workbook('test/test_sheets/test_id_clash.xlsx')
sheet = workbook.sheet_by_index(0)

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

	row_id = row[id_index]
	row_dict = { row_id: {} }
	for i, cell in enumerate(row):
		row_dict[row_id][headers[i]] = cell
	return row_dict

def buildShelveFile(shelf_file_path, sheet, id_column, test=False):
	shelve_file = shelve.open(shelf_file_path)
	headers = getHeaders(sheet)
	for row in getRowData(sheet):
		row = buildRowDict(row, headers, id_column)
		resolveConfict = chooseBetween
		
		if row.keys()[0].encode('ascii') in shelve_file:
			if not test: # Prevents the chooseBetween function from working to test should_not_overwrite option
				shelve_file[row.keys()[0]] = resolveConflict(shelve_file[row.keys()[0]], row[row.keys()[0]], 'A_HEADER')
		else:
			# Just write
			shelve_file[row.keys()[0]] = row[row.keys()[0]]

		## fields to farm out to other file, plus filelocation??
	shelve_file.close()



def chooseBetween(shelve_file_row, row, column_to_compare, select='greater'):
	shelf_row = shelve_file_row
	new_row = row

	if shelf_row[column_to_compare] < new_row[column_to_compare] and select == 'greater':
		return new_row


