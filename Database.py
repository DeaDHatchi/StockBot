__author__ = 'Hatchi'

from StockBot import Symbol

# Stock Text File Format :: Stock Symbol - Bought_Price - Current_Shares
# Account Text File Format :: Account_Balance - Amount_Invested - Gross - Net_Profit - Bought_Count - Sold_Count

'''
        account_item_list[0] :: self.account_balance = 1000000.0
        account_item_list[1] :: self.amount_invested = 0.0
        account_item_list[2] :: self.gross = 0.0
        account_item_list[3] :: self.net_profit = 0.0
        account_item_list[4] :: self.bought_count = 0
        account_item_list[5] :: self.sold_count = 0
'''


class Database:

    def __init__(self):
        self.stock_database_string = []

    def read_file(self):

        stock_text_file = open("stock_database.txt", "r").readlines()
        account_text_file = open("account_database.txt", "r").readline()
        account_item_list = account_text_file.split('-')
        x.account_balance = float(account_item_list[0])
        x.amount_invested = float(account_item_list[1])
        x.gross = float(account_item_list[2])
        x.net_profit = float(account_item_list[3])
        x.bought_count = int(account_item_list[4])
        x.sold_count = int(account_item_list[5])

        for item in stock_text_file:
            try:
                item_list = item.split("-")
                x.symbol = str(item_list[0])
                x.bought_price = float(item_list[1])
                x.current_shares = int(item_list[2])
                x.google_scrape()
                x.buy_or_sell_switch()
                string_input = str(x.symbol) + "-" + str(x.bought_price) + "-" + str(x.current_shares) + "\n"
                self.stock_database_string.append(string_input)
                x.variable_reset()
            except ValueError:
                print("")
                print("ValueError for :: " + str(x.symbol) + " :: Skipping")
                x.variable_reset()
                continue
            except IndexError:
                print("")
                print("IndexError for :: " + str(x.symbol) + " :: Skipping")
                x.variable_reset()
                continue

        x.account_printout()
        x.list_reset()

    def write_file(self):

        stock_text_file = open("stock_database.txt", "w")
        account_text_file = open("account_database.txt", "w")
        account_info = str(x.account_balance) + "-" + str(x.amount_invested) + "-" + str(x.gross) + "-" + \
            str(x.net_profit) + "-" + str(x.bought_count) + "-" + str(x.sold_count) + "\n"

        for item in self.stock_database_string:
            stock_text_file.writelines(item)

        account_text_file.writelines(account_info)

        self.stock_database_string = []

        stock_text_file.close()
        account_text_file.close()

x = Symbol()
y = Database()
y.read_file()
y.write_file()
