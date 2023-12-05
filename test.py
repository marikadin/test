import streamlit as st
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from urllib.parse import urlparse, parse_qs
import yfinance as yf
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

st.title("Stocks")

# Set the minimum and maximum selectable dates
min_date = datetime.date(2022, 1, 1)
max_date = datetime.date.today()

# Get user input for a date within the specified range, with a default value
selected_date = st.date_input("Select a date", min_value=min_date, max_value=max_date, value=min_date)

# Add a text input for stock name
stock_name = st.text_input("Enter Stock Name")

# Function to get search results URL
def get_search_results_url(url, keyword):
    print("Fetching...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yfin-usr-qry')))

        search_bar.clear()

        search_bar.send_keys(keyword)

        search_bar.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        time.sleep(3)

        search_results_url = driver.current_url

        return search_results_url

    finally:
        driver.quit()


# Function to extract stock symbol and historical data
def extract_stock_symbol(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    stock_symbol = query_params.get('p', [''])[0]

    try:
        data = yf.download(stock_symbol, start=min_date, end=datetime.date.today())
    except:
        sys.exit("Couldn't get info.")

    return data['Open'].tolist(), data.index.strftime("%d-%m-%Y").tolist()

# Function for machine learning prediction
def machine_learning_prediction(data):
    data = np.array(data)

    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(data.reshape(-1, 1))

    def create_sequences(data, seq_length):
        sequences, labels = [], []
        for i in range(len(data) - seq_length):
            seq = data[i:i + seq_length]
            label = data[i + seq_length]
            sequences.append(seq)
            labels.append(label)
        return np.array(sequences), np.array(labels)

    seq_length = 10  
    sequences, labels = create_sequences(data_normalized, seq_length)

    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    X_train, y_train = sequences, labels
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    model.fit(X_train, y_train, epochs=50, batch_size=32)

    last_sequence = data_normalized[-seq_length:]
    last_sequence = last_sequence.reshape((1, seq_length, 1))

    predicted_value = model.predict(last_sequence)
    predicted_value = scaler.inverse_transform(predicted_value.reshape(1, -1))[0, 0]

    return predicted_value

# Add a button to proceed
if st.button("Proceed"):
    # Check if stock name is provided
    if not stock_name:
        st.warning("You must enter a stock name!")
    else:
        st.success(f"Stock Name '{stock_name}' saved!")

        # Rest of your code
        website_url = 'https://finance.yahoo.com/'  
        try:
            search_results_url = get_search_results_url(website_url, stock_name)
        except:
            st.write("Thanks for trying. See you soon(:")
            sys.exit()

        if "404" in search_results_url:
            st.warning("Stock is not in Yahoo database.")
            sys.exit()
        elif "https://finance.yahoo.com" not in search_results_url:
            st.warning("Stock is not in Yahoo database.")
            sys.exit()
        elif "news" in search_results_url:
            st.warning("Not a stock but news: " + search_results_url)
            sys.exit()
        elif "/m/" in search_results_url:
            st.warning("Stock is not in Yahoo database.")
            sys.exit()
        elif "/company/" in search_results_url:
            st.warning("A private company: " + search_results_url)
            sys.exit()
        else:
            if search_results_url:
                st.success(f"URL of the search results page for {stock_name}: {search_results_url}")
                
                # Extract stock symbol and historical data
                stock_symbol, date_list = extract_stock_symbol(search_results_url)

                # Machine learning prediction
                predicted_value = machine_learning_prediction(stock_symbol)

                # Display results
                st.write(f"Stock Symbol: {stock_symbol}")
                st.write(f"Predicted Value: {predicted_value}")

                # Display the graph
                fig, ax = plt.subplots()
                ax.plot(date_list, stock_symbol, label='Stock Symbol')
                ax.set_xlabel('Date')
                ax.set_ylabel('Stock Symbol')
                ax.set_title('Stock Symbol Over Time')
                ax.legend()
                st.pyplot(fig)
            else:
                st.warning(f"No search results found for {stock_name}.")
