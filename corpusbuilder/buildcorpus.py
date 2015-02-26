import xlrd as xlrd

workbook = xlrd.open_workbook('test.xlsx')
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


#print(getRowData(sheet))


# OK, so shelf func goes somthing like:
#
#for row in getRowData(sheet):
#		convert row into dict, by wrapping in buildRowDict function
# 	CHECK SHELF FOR SAME NAME && if same page and later timestamp...
#		add to shelf.

# yes...
for row in getRowData(sheet):
	print row


def getDataDict(sheet):
	headers = getHeaders(sheet)
	rows = getRowData(sheet)
	data_dict = {}
	
	# for each row, create new dict
	# for each cell in row, add header and value

	# USE THIS CODE TO WRITE SERIALLY TO SHELF...
	'''
	for row_index, row in enumerate(rows):
		row_dict = {}
		for col_index in range(sheet.ncols):
			row_dict[headers[col_index]] = sheet.cell(row_index+1, col_index).value
		data_dict[row_index] = row_dict

	return data_dict

print getDataDict(sheet)
'''