import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def get_stock_data(symbol):
    try:
        stock_data = yf.download(symbol, start="2022-01-01", end="2023-01-01")
        return stock_data
    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        return None

def plot_stock_data(stock_data):
    fig = px.line(stock_data, x=stock_data.index, y='Close', title='Stock Prices Over the Last Year')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Stock Price (USD)')
    st.plotly_chart(fig)

def main():
    st.title("Stock Price Visualization App")

    stock_name = st.text_input("Enter the stock symbol or company name (e.g., NVDA, AAPL):")

    if stock_name:
        st.write(f"Displaying stock data for {stock_name}")

        stock_data = get_stock_data(stock_name)
        if stock_data is not None:
            plot_stock_data(stock_data)

if __name__ == "__main__":
    main()
