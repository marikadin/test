import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf

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

def predict_tomorrows_stock_value_linear_regression(stock_data):
    # Assuming a simple linear regression model for demonstration
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']

    model = LinearRegression()
    model.fit(X, y)

    # Predict tomorrow's stock value
    tomorrow = X.iloc[[-1]]['Days'].values[0] + 1
    predicted_value = model.predict([[tomorrow]])[0]

    return predicted_value

def predict_tomorrows_stock_value_lstm(stock_data):
    # Normalize the data
    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))

    # Create sequences for LSTM
    seq_length = 10
    sequences, labels = [], []
    for i in range(len(data_normalized) - seq_length):
        seq = data_normalized[i:i + seq_length]
        label = data_normalized[i + seq_length]
        sequences.append(seq)
        labels.append(label)

    X_train, y_train = np.array(sequences), np.array(labels)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    # Build LSTM model
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Generate a new sequence for prediction
    last_sequence = data_normalized[-seq_length:]
    last_sequence = last_sequence.reshape((1, seq_length, 1))

    # Predict tomorrow's stock value using LSTM
    predicted_value = model.predict(last_sequence)
    predicted_value = scaler.inverse_transform(predicted_value.reshape(1, -1))[0, 0]

    return predicted_value

# Streamlit app
st.title("Stock Symbol Lookup and Prediction")

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
            st.title("Stock Price Visualization App")

            if stock_symbol:
                st.write(f"Displaying stock data for {stock_symbol}")

                stock_data = get_stock_data(stock_symbol)
                if stock_data is not None:
                    plot_stock_data(stock_data)

                    # Predict tomorrow's stock value using Linear Regression
                    predicted_value_lr = predict_tomorrows_stock_value_linear_regression(stock_data)
                    st.write(f"Approximate tomorrow's stock value (Linear Regression): ${predicted_value_lr:.2f}")

                    # Predict tomorrow's stock value using LSTM
                    predicted_value_lstm = predict_tomorrows_stock_value_lstm(stock_data)
                    st.write(f"Approximate tomorrow's stock value (LSTM): ${predicted_value_lstm:.2f}")
        else:
            st.warning(f"Could not find the stock symbol for {company_name}")
