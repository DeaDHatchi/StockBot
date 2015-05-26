__author__ = 'Hatchi'

from bs4 import BeautifulSoup
import requests


class Symbol:

    def __init__(self):
        # Hard Coded Values
        self.stock_margin = 0.15
        self.transaction_cost = 7
        self.trade_shares = 100
        self.max_shares = 100
        self.investment_return = 0.15

        # Trade Variables
        self.symbol = ""
        self.current_price = 0.0
        self.current_shares = 0
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

        # List Variables
        self.bought_list = []
        self.sold_list = []

    '''
        c_list array -- 0 = Current Price
        s_list array -- 0 = Range, 1 = 52 week, 2 = Open, 3 = Vol/Avg, 4 = Mkt cap, 5 = P/E
        s_list array -- 6 = Div/yield, 7 = EPS, 8 = Shares, 9 = Beta, 10 = Inst. own
    '''

    # Google Scrape for Stock Information
    def google_scrape(self):
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

    # Buy/Sell Switch based on Current Shares
    def buy_or_sell_switch(self):
        if self.current_shares > 0:
            self.sell_shares()
        else:
            self.buy_shares()

    # Buy Parameters Function
    def buy_shares(self):
        self.buy_target = self.range_52_low + (self.range_52 * self.stock_margin)
        if self.current_price <= self.buy_target and self.current_shares < self.max_shares and self.account_balance > \
                (self.current_price * self.trade_shares) + self.transaction_cost:
            self.bought_price = self.current_price
            self.account_balance -= (self.bought_price * self.trade_shares) + self.transaction_cost
            self.amount_invested += (self.bought_price * self.trade_shares) + self.transaction_cost
            self.current_shares += self.trade_shares
            self.stock_status = "Bought"
            self.bought_count += 1
            self.bought_list.append(self.symbol)
            self.sell_target = self.bought_price + (self.bought_price * self.investment_return) + \
                (self.transaction_cost / self.trade_shares)
            self.print_out()
        else:
            self.stock_status = "Waiting"

    # Sell Parameters Function
    def sell_shares(self):
        self.sell_target = self.bought_price + (self.bought_price * self.investment_return) + \
            (self.transaction_cost / self.trade_shares)
        if self.current_price >= self.sell_target:
            self.amount_invested -= (self.bought_price * self.current_shares) + self.transaction_cost
            self.gross += self.current_price * self.current_shares
            self.net_profit += (self.current_price * self.current_shares) - (self.bought_price * self.current_shares) \
                - (self.transaction_cost * 2)
            self.account_balance += (self.current_price * self.trade_shares) - self.transaction_cost
            self.current_shares -= self.trade_shares
            self.bought_price = 0.0
            self.sold_count += 1
            self.stock_status = "Sold"
            self.sold_list.append(self.symbol)
            self.print_out()
        else:
            self.stock_status = "Waiting"

    # Basic printout of stock information on Buy/Sell
    def print_out(self):
        print("")
        print("-=-=-=-=- " + str(self.symbol) + " -=-=-=-=-")
        print("Current Price: " + str(self.current_price))
        print("Buy Target: " + str(self.buy_target))
        print("Sell Target: " + str(self.sell_target))
        print("Current Value: ") + str(self.current_price * self.current_shares)
        print("Stock Range Low: " + str(self.range_low))
        print("Stock Range High: " + str(self.range_high))
        print("52 Week Range low: " + str(self.range_52_low))
        print("52 Week Range High: " + str(self.range_52_high))
        print("Stock Open: " + str(self.stock_open))
        print("Market Cap: " + str(self.market_cap))
        print("Market Shares: " + str(self.market_shares))
        print("Stock Status: " + str(self.stock_status))
        print("-=-=-=-=-=-=-=-=-=-=-=-")

    # Added for Full Account Details after run 5/26/2015
    def account_printout(self):
        print("")
        print("-=-=-=- Hatchi Account -=-=-=-")
        print("Account Balance: " + str(self.account_balance))
        print("Amount Invested: " + str(self.amount_invested))
        print("Total Bought Count: " + str(self.bought_count))
        print("Total Sold Count: " + str(self.sold_count))
        print("-=-=-=- Bought List -=-=-=-")
        for item in self.bought_list:
            print("::" + item)
        print("-=-=-=- Sold List -=-=-=-")
        for item in self.sold_list:
            print("::" + item)

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

    # Added for List Resets after run completion - 5/26/2015
    def list_reset(self):
        self.bought_list = []
        self.sold_list = []