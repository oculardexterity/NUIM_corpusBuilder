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
		rows.append(row)
	return rows

def getDataDict(sheet):
	headers = getHeaders(sheet)
	rows = getRowData(sheet)
	data_dict = {}
	
	# for each row, create new dict
	# for each cell in row, add header and value
	for row_index, row in enumerate(rows):
		row_dict = {}
		for col_index in range(sheet.ncols):
			row_dict[headers[col_index]] = sheet.cell(row_index+1, col_index).value
		data_dict[row_index] = row_dict

	return data_dict

print getDataDict(sheet)