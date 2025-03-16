import yfinance as yf
import pandas as pd
import time

class TradingBot:
    def __init__(self, symbol, short_window=10, long_window=50, cash=10000):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.cash = cash
        self.holdings = 0
        self.trade_log = []

    def fetch_data(self):
        stock = yf.Ticker(self.symbol)
        data = stock.history(period="60d", interval="1d")
        return data

    def moving_average_strategy(self, data):
        data['Short_MA'] = data['Close'].rolling(window=self.short_window).mean()
        data['Long_MA'] = data['Close'].rolling(window=self.long_window).mean()
        
        if data['Short_MA'].iloc[-1] > data['Long_MA'].iloc[-1] and self.cash > 0:
            self.buy(data['Close'].iloc[-1])
        elif data['Short_MA'].iloc[-1] < data['Long_MA'].iloc[-1] and self.holdings > 0:
            self.sell(data['Close'].iloc[-1])

    def buy(self, price):
        shares = self.cash // price
        self.cash -= shares * price
        self.holdings += shares
        self.trade_log.append(f"Bought {shares} shares at {price}")
        print(f"Bought {shares} shares at {price}")

    def sell(self, price):
        self.cash += self.holdings * price
        self.trade_log.append(f"Sold {self.holdings} shares at {price}")
        print(f"Sold {self.holdings} shares at {price}")
        self.holdings = 0

    def run(self):
        while True:
            data = self.fetch_data()
            self.moving_average_strategy(data)
            time.sleep(60)  

if __name__ == "__main__":
    bot = TradingBot("RR") # Or whatever stock you're looking at
    bot.run()
