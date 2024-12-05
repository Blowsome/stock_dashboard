import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_stock_data import all_data

@st.cache_data
def load_data():
    df = pd.read_csv('./all_data.csv')
    return df
print(all_data.shape)

def show_page(all_data):
    st.title("Stock Line Chart")

    # User input for stock symbol and date range
    ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL):", "AAPL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-12-31"))
    data = all_data[all_data['Ticker']==ticker]
    data['Date']=pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Fetch and display stock data
    if not data.empty:
        st.write(f"Showing data for:")
        st.dataframe(data.head(2))
        st.dataframe(data.tail(2))
        print(data.columns)
        print(data.index)

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
show_page(all_data)