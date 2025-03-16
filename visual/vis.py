import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

symbol = "RR"  # Or whatever stock you're looking at. Here I'm using Rolls Royce, so RR
short_window = 10  # Short moving average window
long_window = 50  # Long moving average window

# Stock data
stock = yf.Ticker(symbol)
data = stock.history(period="6mo", interval="1d")

# Calculate moving averages
data["Short_MA"] = data["Close"].rolling(window=short_window).mean()
data["Long_MA"] = data["Close"].rolling(window=long_window).mean()

# Signals
data["Signal"] = np.where(data["Short_MA"] > data["Long_MA"], 1, 0)  # 1: Buy, 0: Sell/Hold

# IBuy/sell points
data["Buy_Signal"] = (data["Signal"].diff() > 0)  # When short MA crosses above long MA
data["Sell_Signal"] = (data["Signal"].diff() < 0)  # When short MA crosses below long MA

# Stock price and moving averages as a visual
plt.figure(figsize=(14, 7))
plt.plot(data.index, data["Close"], label="Stock Price", color="black", alpha=0.6)
plt.plot(data.index, data["Short_MA"], label=f"{short_window}-Day MA", linestyle="dashed", color="blue")
plt.plot(data.index, data["Long_MA"], label=f"{long_window}-Day MA", linestyle="dashed", color="red")

# Buy/sell points highlighted
plt.scatter(data.index[data["Buy_Signal"]], data["Close"][data["Buy_Signal"]], label="Buy Signal", marker="^", color="green", alpha=1)
plt.scatter(data.index[data["Sell_Signal"]], data["Close"][data["Sell_Signal"]], label="Sell Signal", marker="v", color="red", alpha=1)

plt.title(f"{symbol} Stock Price with Moving Average Strategy")
plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")
plt.legend()
plt.show()

data.tail(30)