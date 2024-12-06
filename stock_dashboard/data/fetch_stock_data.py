import yfinance as yf
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta
from fetch_stock_tickers import full_tickers
from dateutil.relativedelta import relativedelta
import time
from itertools import islice
from pathlib import Path


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
    
    def get_sector_info(self, tickers):
        data = []
        for i, ticker in enumerate(tickers):
            try:
                info = yf.Ticker(ticker).info
                sector = info.get("sector", "N/A")
                industry = info.get("industry", "N/A")
                data.append({"Ticker":ticker, "Sector": sector, "Industry":industry})
            except Exception as e:
                print("Eorr fetching sector/industry info for {ticker}:", {e})
                data.append({"Ticker":ticker, "Sector": "Error", "Industry":"Error"})
            if i%self.batch_size ==0:
                print("step:", i)
                time.sleep(self.delay)
        df = pd.DataFrame(data)
        return df
    
def convert_date_to_str_YYYYMM(df):
    df["Date"] = pd.to_datetime(df["Date"], format='mixed')
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df
    
#downloader = StockData(100,10)
#downloader.recovery_download(start='2022-01-01', interval="1d")

script_dir = Path(__file__).parent
price_dir = script_dir/"assets/all_data.csv"
sector_dir = script_dir/"assets/all_sectors.csv"

all_price_data = pd.read_csv(price_dir)
sector_data = pd.read_csv(sector_dir)

# downloader = StockData(100,60)
#tickers = all_data['Ticker'].unique().tolist()
#sector = downloader.get_sector_info(tickers)
#save_dir = script_dir/"assets/all_sectors.csv"
#sector.to_csv(save_dir, index=False)

# recover tickers with industry and sector error during first download
#all_sectors = pd.read_csv(save_dir)
#error_tickers = all_sectors[all_sectors['Sector']=='Error']['Ticker'].tolist()

#downloader = StockData(100,60)
#tickers_error_sectors = downloader.get_sector_info(error_tickers)

#all_sector = all_sectors[all_sectors['Sector']!='Error'].copy()
#all_sector = pd.concat([all_sector, tickers_error_sectors])
#all_sector.to_csv(save_dir, index=False)


    
