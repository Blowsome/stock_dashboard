import yfinance as yf
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta
from fetch_stock_tickers import full_tickers
from dateutil.relativedelta import relativedelta
import time
from itertools import islice

class StockData:
    """
    Class object to download all kinds of stock data (e.g., price, PE ratio)
    """
    def __init__(self, batch_size: int, delay: int):
        """
        Iniatialize the StockData with a list of ticker symbol
        """
        self.batch_size = batch_size
        self.delay = delay
    def download_tickers_with_batch_delay(self, ticker_symbols: List, **kwargs):
        all_data = []
        invalid_tickers = {}
        for i, ticker in enumerate(ticker_symbols, start=1):
            try:
                data = yf.download(ticker, **kwargs)
                if not data.empty:
                    data['Ticker']=ticker
                    data.columns = ['Adj Close', 'Close','High','Low','Open','Volume', 'Ticker']
                    data.reset_index(inplace=True)
                    all_data.append(data)
                else:
                    invalid_tickers[ticker]='None'
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                invalid_tickers[ticker]=e
            if i%self.batch_size ==0:
                time.sleep(self.delay)
        
        if all_data:
            stock_data = pd.concat(all_data)
        else:
            stock_data = pd.Dataframe()
        invalid_tickers = pd.DataFrame(list(invalid_tickers.items()), columns=["Ticker", "Error_code"])
        return stock_data, invalid_tickers
    def fresh_download(self,**kwargs):
        """
        Download the data from scratch. Currently set the default start date as 2022-01-01
        """
        tickers = full_tickers['Ticker'].tolist()
        stock_data, invalid_tickers = self.download_tickers_with_batch_delay(ticker_symbols = tickers, **kwargs)
        print(stock_data.memory_usage(deep=True).sum()/(1024**2))
        stock_data.to_csv('./all_data.csv', index=False)
        invalid_tickers.to_csv('./invalid_tickers.csv', index=False)
    def recovery_download(self, **kwargs):
        """
        Download the data that are missing from first download - recovery
        """
        try:
            tickers = pd.read_csv('./invalid_tickers.csv')['Ticker'].tolist()
            stock_data, invalid_tickers = self.download_tickers_with_batch_delay(ticker_symbols = tickers, **kwargs)
            initial_batch = pd.read_csv('./all_data.csv')
            stock_data = pd.concat([initial_batch, stock_data])
            stock_data.to_csv('./all_data.csv', index=False)
            print(stock_data.shape)
            print(invalid_tickers.shape)
        except Exception as e:
            print(f"Error fetching data from recovery pool: {e}")
    def continued_download(self, **kwargs):
        """
        Download the new data on top of already downloaded data and combine to save time.
        """
        try:
            initial_batch = pd.read_csv('./all_data.csv')  
            tickers = initial_batch['Ticker'].tolist()
            last_date = datetime.strptime(initial_batch['Date'].max(), "%Y-%m-%d")
            new_start_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
            stock_data, invalid_tickers = self.download_tickers_with_batch_delay(ticker_symbols = tickers, start= new_start_date, **kwargs)
            stock_data = pd.concat([initial_batch, stock_data]).sort_values(by=['Ticker','Date'])
            print(stock_data.shape)
            print(invalid_tickers.shape)
        except Exception as e:
            print(f"Error continuing fetching data: {e}")

def convert_date_to_str_YYYYMM(df):
    df["Date"] = pd.to_datetime(df["Date"], format='mixed')
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df
    
#downloader = StockData(100,10)
#downloader.recovery_download(start='2022-01-01', interval="1d")

all_data = pd.read_csv('./all_data.csv')
    
