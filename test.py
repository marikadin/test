import streamlit as st
import yahooquery as yq
import yfinance as yf
import pandas as pd
import plotly.express as px

def get_stock_symbol(company_name):
    try:
        response = yq.search(company_name)
        if response and 'quotes' in response and response['quotes']:
            return response['quotes'][0]['symbol']
        else:
            st.error(f"Could not find stock symbol for {company_name}")
            return None
    except Exception as e:
        st.error(f"Error retrieving stock symbol: {e}")
        return None

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

    company_name = st.text_input("Enter the company name (e.g., Nvidia, Apple):")

    if company_name:
        st.write(f"Displaying stock data for {company_name}")

        stock_symbol = get_stock_symbol(company_name)
        if stock_symbol:
            stock_data = get_stock_data(stock_symbol)
            if stock_data is not None:
                plot_stock_data(stock_data)

if __name__ == "__main__":
    main()
