__author__ = 'Hatchi'

from bs4 import BeautifulSoup
import requests
import xlrd


class Symbol:

    def __init__(self):
        # Hard Coded Values
        self.stock_symbol_list = []
        self.stock_margin = 0.15
        self.transaction_cost = 7
        self.trade_shares = 100
        self.max_shares = 100
        self.investment_return = 0.15

        # Trade Variables
        self.symbol = ""
        self.current_price = 0.0
        self.current_shares = 0
        self.bought_shares = 0
        self.stock_open = 0.0
        self.range_low = 0.0
        self.range_high = 0.0
        self.range_52_high = 0.0
        self.range_52_low = 0.0
        self.market_cap = ""
        self.market_shares = ""
        self.range_52 = 0.0
        self.buy_target = 0.0
        self.bought_price = 0.0
        self.sell_target = 0.0
        self.sell_price = 0.0
        self.stock_status = ""

        # Account Variables
        self.account_balance = 1000000.0
        self.amount_invested = 0.0
        self.gross = 0.0
        self.net_profit = 0.0
        self.bought_count = 0
        self.sold_count = 0

    def execute(self):
        self.excel_database(input("File Location: "))
        self.scrape_trigger()
        self.account_printout()

    def excel_database(self, file_location):
        workbook = xlrd.open_workbook(file_location)
        sheet = workbook.sheet_by_index(0)

        for row in range(sheet.nrows):
            stock_symbol = sheet.cell_value(row, 1)
            self.stock_symbol_list.append(stock_symbol)

    # Added Error Handling for Value + Index Errors on Scrapes - Skips - 5/22/2015
    def scrape_trigger(self):
        for symbol in self.stock_symbol_list:
            try:
                self.scrapes(symbol)
            except ValueError:
                print("")
                print("ValueError for :: " + str(self.symbol) + " :: Skipping")
                self.variable_reset()
                continue
            except IndexError:
                print("")
                print("IndexError for :: " + str(self.symbol) + " :: Skipping")
                self.variable_reset()
                continue

    def scrapes(self, symbol):
        self.google_scrape(symbol)
        self.buy_or_sell_switch()
        # Add self.Save()
        self.variable_reset()

    '''
        c_list array -- 0 = Current Price
        s_list array -- 0 = Range, 1 = 52 week, 2 = Open, 3 = Vol/Avg, 4 = Mkt cap, 5 = P/E
        s_list array -- 6 = Div/yield, 7 = EPS, 8 = Shares, 9 = Beta, 10 = Inst. own
    '''

    def google_scrape(self, symbol):
        self.symbol = symbol
        r = requests.get("https://www.google.com/finance?q=" + self.symbol)
        data = r.text
        soup = BeautifulSoup(data)
        tag = soup.div
        c_data = tag.find_all("span", {"class": "pr"})
        t_data = tag.find_all("td", {"class": "val"})
        c_list = []
        s_list = []
        for object_in in c_data:
            stock_current_price = object_in.text.strip()
            c_list.append(stock_current_price)
        for object_in in t_data:
            stock_table = object_in.text.strip()
            s_list.append(stock_table)
        week_range = s_list[0].split(" - ")
        for item in week_range:
            item.strip('-')
            item.strip(',')
        self.range_low = float(week_range[0])
        self.range_high = float(week_range[1])
        range_52 = s_list[1].split(" - ")
        self.range_52_low = float(range_52[0])
        self.range_52_high = float(range_52[1])
        self.range_52 = self.range_52_high - self.range_52_low
        self.current_price = float(c_list[0])
        self.stock_open = float(s_list[2])
        self.market_cap = s_list[4]
        self.market_shares = s_list[8]

    def buy_or_sell_switch(self):
        if self.current_shares > 0:
            self.sell_shares()
        else:
            self.buy_shares()

    def buy_shares(self):
        self.buy_target = self.range_52_low + (self.range_52 * self.stock_margin)
        if self.current_price <= self.buy_target and self.current_shares < self.max_shares and self.account_balance > \
                (self.current_price * self.trade_shares) + self.transaction_cost:
            self.bought_price = self.current_price
            self.account_balance -= (self.bought_price * self.trade_shares) + self.transaction_cost
            self.amount_invested += (self.bought_price * self.trade_shares) + self.transaction_cost
            self.bought_shares += self.trade_shares
            self.stock_status = "Bought"
            self.bought_count += 1
            self.print_out()
        else:
            self.stock_status = "Waiting"

    def sell_shares(self):
        self.sell_target = self.bought_price + (self.bought_price * self.investment_return) + \
            (self.transaction_cost / self.trade_shares)
        if self.current_price >= self.sell_target:
            self.amount_invested -= (self.bought_price * self.trade_shares) + self.transaction_cost
            self.gross += self.current_price * self.current_shares
            self.net_profit += (self.current_price * self.current_shares) - (self.bought_price * self.current_shares) \
                - (self.transaction_cost * 2)
            self.account_balance += (self.current_price * self.trade_shares) - self.transaction_cost
            self.current_shares -= self.trade_shares
            self.stock_status = "Sold"
            self.sold_count += 1
            self.print_out()
        else:
            self.stock_status = "Waiting"

    def print_out(self):
        print("")
        print("-=-=-=-=- " + str(self.symbol) + " -=-=-=-=-")
        print("Current Price: " + str(self.current_price))
        print("Buy Target: " + str(self.buy_target))
        print("Stock Range Low: " + str(self.range_low))
        print("Stock Range High: " + str(self.range_high))
        print("52 Week Range low: " + str(self.range_52_low))
        print("52 Week Range High: " + str(self.range_52_high))
        print("Stock Open: " + str(self.stock_open))
        print("Market Cap: " + str(self.market_cap))
        print("Market Shares: " + str(self.market_shares))
        print("Stock Status: " + str(self.stock_status))
        print("-=-=-=-=-=-=-=-=-=-=-=-")

    def account_printout(self):
        print("")
        print("-=-=-=- Hatchi Account -=-=-=-")
        print("Account Balance: " + str(self.account_balance))
        print("Amount Invested: " + str(self.amount_invested))
        print("Bought Count: " + str(self.bought_count))
        print("Bought Shares: " + str(self.bought_shares))
        print("Sold Count: " + str(self.sold_count))
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    # Added for Variable Resets after scrape - 5/22/2015
    def variable_reset(self):
        self.symbol = ""
        self.current_price = 0
        self.current_shares = 0
        self.stock_open = 0
        self.range_low = 0
        self.range_high = 0
        self.range_52_high = 0
        self.range_52_low = 0
        self.market_cap = ""
        self.market_shares = ""
        self.range_52 = 0
        self.buy_target = 0
        self.bought_price = 0
        self.sell_target = 0
        self.sell_price = 0
        self.stock_status = ""


x = Symbol()
x.execute()
# C:\Users\Travis\Documents\GitHub\StockBot\StockSymbolList.xls
# C:\Users\Travis\Documents\GitHub\StockBot\StockSymbolList_test.xls