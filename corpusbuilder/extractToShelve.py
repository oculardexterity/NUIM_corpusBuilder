import os
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
	if os.path.isfile(shelf_file_path):
			os.remove(shelf_file_path)

	shelve_file = shelve.open(shelf_file_path)
	headers = getHeaders(sheet)

	for row in getRowData(sheet):
		row = buildRowDict(row, headers, id_column)

		current_row_key = str(row.keys()[0].encode('ascii'))
		#print shelve_file

		if str(row.keys()[0].encode('ascii')) in shelve_file:
			if not test: # Prevents the chooseBetween function from working to test should_not_overwrite_existing
				#print 'FOUND TRUE'

				row_to_write = chooseBetween(shelve_file[current_row_key], row[current_row_key], conflict_res_column)

				shelve_file[current_row_key] = row_to_write
				#print 'replace'
		else:
			# Just write
			#print 'FOUND FALSE'
			shelve_file[row.keys()[0]] = row[row.keys()[0]]
			#print 'write'
		#print 'SHELF AFTER ', shelve_file[current_row_key], type(shelve_file)

	


def chooseBetween(shelf_row, new_row, column_to_compare):
	#print 'CHOOSEBETWEENROW: ', shelf_row['Translation_Timestamp']
	#print 'NEW_ROW ', new_row['Translation_Timestamp']
	#print shelf_row

	if shelf_row[column_to_compare] < new_row[column_to_compare]:
		return new_row
	else:
		return shelf_row

	"""
	if shelf_row[column_to_compare] < new_row[column_to_compare] and select == 'greater':
		print '---------------REPLACED----------'
		return new_row
	elif shelf_row[column_to_compare] < new_row[column_to_compare] and select == 'lesser':
		print '---------------CURRENT ROW----------'
		return shelf_row
	"""

def main():
	buildShelveFile(shelveFile, sheet, id_column, 'Translation_Timestamp')


if __name__ == "__main__":
	main()

