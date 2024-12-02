import yfinance as yf
import pandas as pd
from typing import List, Optional

class StockData:
    """
    Class object to download all kinds of stock data (e.g., price, PE ratio)
    """
    def __init__(self, ticker_symbols: List[str]):
        """
        Iniatialize the StockData with a list of ticker symbol
        """
        self.ticker_symbols = ticker_symbols

    def get_price_data(self, period: str = 'max', interval: str = '1d'):
        """
        Download historical stock price data

        Parameters:
        - period (str): The period of historical data (e.g., '1d', '1mo', '1y', 'max').
        - interval (str): The interval between data points (e.g., '1d','1h')

        Returns:
        - pd.DataFrame: Historical stock price dataframe
        """
        try:
            data = yf.download(self.ticker_symbols, group_by='Ticker', 
                               period=period,
                               interval = interval)
            data = data.stack(level=0, future_stack=True).rename_axis(['Date', 'Ticker']).reset_index(level=1)
            return data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()

stock_data = None
if stock_data is None:        
    downloader = StockData(['AAPL', 'GOOG','TSLA'])
    stock_data = downloader.get_price_data()
else:
    pass