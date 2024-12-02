import streamlit as st
from download import stock_data
import pandas as pd
import matplotlib.pyplot as plt

def show_page():
    st.title("Data Viewer")

    # Fetch and clean data
    df = stock_data.head(5)

    # Display data
    st.write("Raw Data:")
    st.dataframe(df)

data = stock_data
def show_page(data):
    st.title("Stock Line Chart")

    # User input for stock symbol and date range
    ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL):", "AAPL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-12-31"))
    data = data[data['Ticker']=='AAPL']

    # Fetch and display stock data
    if not data.empty:
        st.write(f"Showing data for:")
        st.dataframe(data.head(2))
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
show_page(data)