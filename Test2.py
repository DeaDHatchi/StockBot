__author__ = 'Travis'

from StockBot import Symbol

x = Symbol()

text_file = open("write_it.txt", "r")

# Item Format :: Stock Symbol :: Bought_Price :: Bought_Shares :: Sell_Target

stock_list = []

for item in text_file:
    item.split("-")
    item.strip("\n")
    x.symbol = str(item[0])
    x.bought_price = int(item[1])
    x.bought_shares = int(item[2])
    x.google_scrape(x.symbol)
    xString = str(x.symbol) + str(x.bought_price) + str(x.bought_shares) + "\n"
    stock_list.append(xString)

text_file.close()

text_file_write = open("write_it.txt", "w")

for item in stock_list:
    text_file_write.writelines(item)

text_file.close()

# C:\Users\Travis\Documents\StockSymbolList.xls