__author__ = 'Travis'

import xlrd

stock_symbol_list = []


def excel_database(file_location):
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)

    for row in range(sheet.nrows):
        stock_symbol = sheet.cell_value(row, 1)
        stock_symbol_list.append(stock_symbol)

excel_database(input("File Location: "))

text_file = open("write_it.txt", "w")

for item in stock_symbol_list:
    text_file.writelines(item + "-" + "0" + "-" + "0" + "\n")

text_file = open("write_it.txt", "r")
print(text_file.read())
text_file.close()

# C:\Users\Travis\Documents\StockSymbolList.xls