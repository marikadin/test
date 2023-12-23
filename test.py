import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf
import time  
import datetime
import threading

check = False
data=[]
Money_list = []
New_Money_list = []
Name_list = []
button_pressed = False

api_keys = ['MNI5T6CU7KLSFJA8', 'QJFF49AEUN6NX884', '9ZZWS60Q2CZ6JYUK']
current_api_key_index = 0

def main():
    

    page = st.sidebar.radio("Select Page", ["Home", "Stock Analysis","real time stock investment"])

    if page == "Home":
        show_home_page()
    elif page == "Stock Analysis":
        show_stock_analysis_page()
    elif page == "real time stock investment":
            show_real_time_investment_page()

def show_home_page():
    st.title("Stock Analyzer")
    st.write("Welcome to the Stock Analyzer app!")
    st.write("Choose 'Stock Analysis' from the sidebar to start analyzing stocks.")


def show_real_time_investment_page():
    global button_pressed, Money_list, New_Money_list, Name_list

    if not button_pressed:
        all_investments()
    else:
        st.title("Real time stock price change")
        company_name = st.text_input("Enter company name or item:")
        money_invested = st.number_input("How much money did you invest", value=0, step=1, key="money_invested_key")
        start_date = st.date_input("Select start date", datetime.date(2022, 1, 1))
        end_date = datetime.datetime.now().date()

        money_invested_value = st.empty()  # Added this line

        if st.button("Get Stock Symbol"):
            if company_name == "" or money_invested is None:
                st.warning("You have to enter a stock and a money amount.")
            else:
                stock_symbol = get_stock_symbol(company_name)
                if stock_symbol:
                    st.title("Stock Price Visualization App")
                    st.write(f"Displaying stock data for {stock_symbol}")

                    stock_data, start_price, last_price = get_stock_data(stock_symbol, start_date, end_date)
                    if stock_data is not None:
                        percent_change = ((last_price - start_price) / abs(start_price)) * 100
                        changed_money = money_invested + (money_invested * (percent_change / 100))
                        st.write(f"Money invested: ${money_invested:.2f}")
                        st.write(f"Invested money today: ${changed_money:.2f}")
                        Money_list.append(money_invested)
                        New_Money_list.append(changed_money)
                        Name_list.append(stock_symbol)
                        button_pressed = False
                        all_investments()

        money_invested_value.number_input("How much money did you invest", value=money_invested, step=1, key="money_invested_key")

                            
def all_investments():
    global button_pressed, Money_list, New_Money_list, Name_list

    button_placeholder = st.empty()

    if button_placeholder.button("Add investment", key="add_investment"):
        button_pressed = True
        show_real_time_investment_page()

    if not Money_list:
        st.write("You don't have any investments")
    else:
        for i in range(len(Money_list)):
            st.write(f"Invested money: {Money_list[i]}\nInvested money today: {New_Money_list[i]}\nProfit: {New_Money_list[i] - Money_list[i]}")

    if button_pressed:
        button_placeholder.empty()

def get_stock_symbol(company_name):
    for _ in range(len(api_keys)):
        api_key = rotate_api_key()
        base_url = "https://www.alphavantage.co/query"
        function = "SYMBOL_SEARCH"

        params = {
            "function": function,
            "keywords": company_name,
            "apikey": api_key,
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if "bestMatches" in data and data["bestMatches"]:
                # Convert the symbol to uppercase before returning
                stock_symbol = data["bestMatches"][0]["1. symbol"].upper()
                return stock_symbol
        except Exception as e:
            st.error(f"Error: {e}")

    return None
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        
        if stock_data.empty:
            st.warning(f"No data available for symbol {symbol} in the specified date range.")
            return None, None, None

        start_price = stock_data['Open'].iloc[0] if len(stock_data) > 0 else None
        last_price = stock_data['Close'].iloc[-1] if len(stock_data) > 0 else None

        return stock_data, start_price, last_price
    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        return None, None, None
def rotate_api_key():
    global current_api_key_index
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)
    return api_keys[current_api_key_index]
main()