import shelve
import xlrd as xlrd

#MOVE THESE TO MAIN!!
#workbook = xlrd.open_workbook('test/test_sheets/test_simple.xlsx')
#sheet = workbook.sheet_by_index(0)

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

def buildShelveFile(shelf_file_path, sheet, id_column):
	shelve_file = shelve.open(shelf_file_path)
	headers = getHeaders(sheet)
	for row in getRowData(sheet):
		row = buildRowDict(row, headers, id_column)

		# id conflict detector... simple:
			# conflict resolver on some other ChARACTERISTIC??
		# id conflict resolver ....
		'''
		# HERE check id of column, if same, check timestamp
		# of shelved version ...
		# if shelve_file.has_key... ? check timestamp
		'''
		#THIS bit here more useful as automatically overwrites.
		# ... and, if there are NO CONFLICTS, 
		#doesn't care that it overwrites

		# Assuming there are duplications... make more
		# general 

		shelve_file[row.keys()[0]] = row[row.keys()[0]]

		## fields to farm out to other file, plus filelocation??
	shelve_file.close()

#print(getRowData(sheet))


# OK, so shelf func goes somthing like:
#
#for row in getRowData(sheet):
#		convert row into dict, by wrapping in buildRowDict function
# 	CHECK SHELF FOR SAME NAME && if same page and later timestamp...
#		add to shelf.

# yes...


#for row in getRowData(sheet):
#	print row
'''

def getDataDict(sheet):
	headers = getHeaders(sheet)
	rows = getRowData(sheet)
	data_dict = {}
	
	# for each row, create new dict
	# for each cell in row, add header and value

	# USE THIS CODE TO WRITE SERIALLY TO SHELF...
	
	for row_index, row in enumerate(rows):
		row_dict = {}
		for col_index in range(sheet.ncols):
			row_dict[headers[col_index]] = sheet.cell(row_index+1, col_index).value
		data_dict[row_index] = row_dict

	return data_dict

print getDataDict(sheet)
'''