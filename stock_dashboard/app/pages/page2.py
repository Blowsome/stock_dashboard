import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_stock_data import all_price_data, sector_data

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

def show_page(all_data):
    st.title("Stock Line Chart")

    # User input for stock symbol and date range
    ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL):", "AAPL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-12-31"))
    data = all_data[all_data['Ticker']==ticker]
    data['Date']=pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    print(data.shape)

    # Fetch and display stock data
    if not data.empty:
        print('True')
        st.write(f"Showing data for:")
        st.dataframe(data.head(2))
        st.dataframe(data.tail(2))

        # Plotting the stock's closing price
        st.write("Closing Price Line Chart:")
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data["Close"], label="Close Price", color="blue")
        plt.title(f"{ticker} Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)  # Display the chart in Streamlit
    else:
        st.error("No data available for the selected ticker and date range.")
show_page(all_price_data)

