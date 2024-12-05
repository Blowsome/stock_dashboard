import requests
import pandas as pd
from io import StringIO

def fetch_all_ticker(url: str =  "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/refs/heads/main/all/all_tickers.txt")->pd.DataFrame:
    """
    fetch all ticker symbols from a public GitHub repo
    Parameters:
    - url: the web link of the txt file of all ticker symbols

    Returns:
    - A Pandas Dataframe with column of 'Ticker'
    """
    response = requests.get(url)
    if response.status_code == 200:
        # Convert the content to a string
        txt_data = response.text
    else:
        print("Failed to fetch the file:", response.status_code)
        exit()
    tickers = pd.read_csv(StringIO(txt_data), delimiter="\t", header = None, names = ['Ticker'])
    return tickers

full_tickers = fetch_all_ticker()
