import streamlit as st
import requests
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
def get_stock_symbol(api_key, company_name):
    base_url = "https://www.alphavantage.co/query"
    function = "SYMBOL_SEARCH"
    
    # Make the API request
    params = {
        "function": function,
        "keywords": company_name,
        "apikey": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # Extract the stock symbol from the API response
        if "bestMatches" in data and data["bestMatches"]:
            stock_symbol = data["bestMatches"][0]["1. symbol"]
            return stock_symbol
        else:
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app
st.title("Stock Symbol Lookup")

# Input for company name
company_name = st.text_input("Enter company name or item:")

# Button to trigger the stock symbol lookup
if st.button("Get Stock Symbol"):
    # Replace 'YOUR_API_KEY' with the actual API key you obtained from Alpha Vantage
    api_key = 'QJFF49AEUN6NX884'

    if api_key == 'YOUR_API_KEY':
        st.warning("Please replace 'YOUR_API_KEY' with your actual Alpha Vantage API key.")
    elif not company_name:
        st.warning("Please enter a company name or item.")
    else:
        stock_symbol = get_stock_symbol(api_key, company_name)
        if stock_symbol:
            def main():
                st.title("Stock Price Visualization App")
                global stock_symbol
                if stock_symbol:
                    st.write(f"Displaying stock data for {stock_symbol}")

                    stock_data = get_stock_data(stock_symbol)
                    if stock_data is not None:
                        plot_stock_data(stock_data)
        else:
            st.warning(f"Could not find the stock symbol for {company_name}")
if __name__ == "__main__":
    main()
