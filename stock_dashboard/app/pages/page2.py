import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_stock_data import all_price_data, sector_data
import seaborn as sns
import numpy as np

print('Page 2:', all_price_data.shape)
print(sector_data.shape)

def nowrmalize_stock_price(df, price, normalized_price):
    """
    This functions normalize the stock price so that the first date stock price is always one.
    """
    df = df.sort_values(by=['Ticker','Date'])
    df[normalized_price]=df.groupby('Ticker')[price].transform(lambda x:x/x.iloc[0])
    return df

all_price_data = nowrmalize_stock_price(all_price_data, 'Close', 'Close').copy()

show_individual_stock = True

def show_page(all_data):
    st.title("Stock Line Chart")

    # User input for stock symbol and date range
    sector = st.selectbox('Choose a Sector', sector_data['Sector'].unique())

    data = all_data[all_data['Ticker'].isin(sector_data[sector_data['Sector']==sector]['Ticker'].unique())]
    data['Date']=pd.to_datetime(data['Date'])

    # Group by Date and calculate the mean, 25th percentile and 75th percentile for stock price
    daily_stats = data.groupby('Date')['Close'].agg(['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]).reset_index()
    daily_stats.columns = ['Date', 'Mean Price', '25th Percentile', '75th Percentile']

    if not daily_stats.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=daily_stats, x='Date', y='Mean Price', label='Mean Price', color='blue')
        sns.lineplot(data=daily_stats, x='Date', y='25th Percentile', label='25th Percentile', color='green', linestyle='--')
        sns.lineplot(data=daily_stats, x='Date', y='75th Percentile', label='75th Percentile', color='red', linestyle='--')

        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.title('Stock Price Trends with Percentiles')
        plt.legend()

        # Display the plot
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)  # Display the chart in Streamlit

    ticker = np.random.choice(sector_data[sector_data['Sector']==sector]['Ticker'].unique())
    individual_data = all_data[all_data['Ticker']==ticker]
    individual_data['Date']=pd.to_datetime(individual_data['Date'])

    # Fetch and display stock data
    if show_individual_stock:
        # Plotting the stock's closing price
        st.write("Closing Price Line Chart:")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=individual_data, x='Date', y='Close', label='Close', color='blue')
        plt.title(f"{ticker} Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)  # Display the chart in Streamlit
    #else:
    #    st.error("No data available for the selected ticker and date range.")
show_page(all_price_data)

