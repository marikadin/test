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
import random
import json
import os
from googletrans import Translator
from login import sign_in, sign_up, user_exists

check = False

data = []

api_keys = ['MNI5T6CU7KLSFJA8', 'QJFF49AEUN6NX884', '9ZZWS60Q2CZ6JYUK', 'ZX5XTAKCAXGAYNBG', "XUKT2LY2NIC35B83",
            "9XZBYP0RSJFMOT4L"
    , "L485NGI7NK2M6VFT", "PS74H4D0OXVW2M22", "X7RFFB0EHKNTH25O", "EEINBBF6PX2GAO02", "FLTAY1Z6W73ZVRQB",
            "JDZLDTK95XWAYVEP"
    , "QOHMIEDH92482YHC", "ZL7O0XZCYX1QQAIB"]
api_key = api_keys[random.randint(0, len(api_keys) - 1)]


def get_stock_symbol_from_json(company_name):
    try:
        with open("stocks.json", "r") as json_file:
            data = json.load(json_file)
            if company_name in data:
                return data[company_name]
    except FileNotFoundError:
        pass  # File not found, proceed to API call
    except json.JSONDecodeError:
        pass  # JSON decoding error, proceed to API call

    return None


def update_stock_symbol_in_json(company_name, stock_symbol):
    try:
        with open("stocks.json", "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[company_name] = stock_symbol

    with open("stocks.json", "w") as json_file:
        json.dump(data, json_file)


def get_stock_symbol(company_name):
    global api_key

    stock_symbol = get_stock_symbol_from_json(company_name)

    if stock_symbol:
        return stock_symbol

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
            stock_symbol = data["bestMatches"][0]["1. symbol"].upper()

            # Update JSON file with the new entry
            update_stock_symbol_in_json(company_name, stock_symbol)

            return stock_symbol
    except Exception as e:
        st.error(f"Error: {e}")

    return None


def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)

        # Check if the retrieved data is empty
        if stock_data.empty:
            st.warning("No data available for the specified date range.")
            return None

        # Check if there are missing values in the data
        if stock_data.isnull().values.any():
            st.warning("Data contains missing values. Please check the data for completeness.")
            return None

        return stock_data
    except yf.YFinanceError as yf_error:
        # Handle the specific exception related to the failed download
        if "No timezone found, symbol may be delisted" in str(yf_error):
            st.warning(f"Error retrieving data: {yf_error}. The symbol may be delisted.")
        else:
            st.error(f"Error retrieving data: {yf_error}")

        return None


def plot_stock_data(stock_data):
    fig = px.line(stock_data, x=stock_data.index, y='Close', title='Stock Prices Over the Last Year')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Stock Price (USD)')
    st.plotly_chart(fig)


def predict_tomorrows_stock_value_linear_regression(stock_data):
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']

    model = LinearRegression()
    model.fit(X, y)

    tomorrow = X.iloc[[-1]]['Days'].values[0] + 1
    predicted_value = model.predict([[tomorrow]])[0]
    check1 = True
    return predicted_value


def predict_tomorrows_stock_value_lstm(stock_data):
    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))

    seq_length = 10
    sequences, labels = [], []
    for i in range(len(data_normalized) - seq_length):
        seq = data_normalized[i:i + seq_length]
        label = data_normalized[i + seq_length]
        sequences.append(seq)
        labels.append(label)

    X_train, y_train = np.array(sequences), np.array(labels)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    model.fit(X_train, y_train, epochs=50, batch_size=32)

    last_sequence = data_normalized[-seq_length:]
    last_sequence = last_sequence.reshape((1, seq_length, 1))

    predicted_value = model.predict(last_sequence)
    predicted_value = scaler.inverse_transform(predicted_value.reshape(1, -1))[0, 0]
    check = True
    return predicted_value


# Function to display information about LSTM
def display_lstm_info():
    st.markdown("""
        Long Short-Term Memory (LSTM) is a type of recurrent neural network (RNN) architecture that is designed to overcome the limitations of traditional RNNs in capturing long-term dependencies in sequential data. RNNs, in theory, can learn from past information to make predictions on future data points, but in practice, they often struggle to learn and remember information from distant past time steps due to the vanishing gradient problem.

LSTM was introduced to address the vanishing gradient problem by incorporating memory cells and gating mechanisms. The key components of an LSTM cell include:

1. **Cell State (Ct):** This is the memory of the cell. It can retain information over long sequences, allowing the model to capture long-term dependencies.

2. **Hidden State (ht):** This is the output of the cell and is used for making predictions. It can selectively expose parts of the cell state.

3. **Three Gates:**
   - **Forget Gate (ft):** Decides what information to throw away from the cell state.
   - **Input Gate (it):** Updates the cell state with new information.
   - **Output Gate (ot):** Controls what parts of the cell state should be output.

LSTM's ability to selectively learn, forget, and store information makes it particularly effective for tasks involving sequences, such as time series forecasting, natural language processing, and speech recognition.

In the context of time series prediction, like predicting stock prices, LSTM models are well-suited to capture patterns and dependencies in historical data and make predictions for future values based on that learned context.
    """)


def linear_Regression(stock_data):
    st.markdown("""
Linear regression is a statistical method used for modeling the relationship between a dependent variable and one or more independent variables by fitting a linear equation to the observed data. The most common form is simple linear regression, which deals with the relationship between two variables, while multiple linear regression deals with two or more predictors.

The linear regression equation has the form:

Y =  β(0)+ β(1)X(1) + β(2)X(2) + ... + β(n)x(n) +  ε

Here:
- Y  is the dependent variable.
- X(1), X(2), ..., X(n) are independent variables.
- β(0) is the intercept.
- β(1), β(2)...,β(N) are the coefficients representing the relationship between the independent variables and the dependent variable.
- ε is the error term, representing the unobserved factors that affect the dependent variable.

The goal of linear regression is to find the values of the coefficients that minimize the sum of the squared differences between the observed and predicted values. Once the model is trained, it can be used to make predictions for new data.

Linear regression is widely used in various fields for tasks such as predicting stock prices, housing prices, sales forecasting, and many other applications where understanding the relationship between variables is crucial.  
                """)
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']
    data = y
    model = LinearRegression()
    model.fit(X, y)

    # Predictions for the entire range
    predictions = model.predict(X)

    # Plot the actual and predicted values
    fig_lr = px.line(X, x='Days', y=y, title='Actual vs Predicted (Linear Regression)')
    fig_lr.add_scatter(x=X['Days'], y=predictions, mode='lines', name='Predicted')
    fig_lr.update_xaxes(title_text='Days')
    fig_lr.update_yaxes(title_text='Stock Price (USD)')

    st.plotly_chart(fig_lr)
    m = (y.iloc[-1] - y.iloc[0]) / 707
    st.write("The y(x) linear function:")
    st.write(f"Y = {float(m)}x + {float(y.iloc[0])}")


st.set_page_config(
    page_title="Stocks analyzer",
    page_icon=r"icons8-stock-48.png",

)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


def load_company_dict():
    try:
        with open("stocks.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


company_dict = load_company_dict()


def stockanalyzer():
    st.title("Stock Analyzer")

    company_name = st.selectbox("Select or enter company name:", list(company_dict.keys()), index=0).upper()

    min_date = datetime.date(2022, 1, 1)
    max_date = datetime.datetime.now() - datetime.timedelta(days=16)
    start_date = st.date_input("Select start date:",
                               min_value=min_date,
                               max_value=max_date,
                               value=min_date)

    end_date = datetime.datetime.now().date()

    st.button('Analyze', on_click=click_button)
    if st.session_state.clicked:
        if company_name == "":
            st.warning("You have to enter a stock or a company name.")
        else:
            if company_name.upper() == "APPLE" or company_name.upper() == "AAPL" or company_name.upper() == "APLE":
                stock_symbol = "AAPL"
            elif company_name.upper() == "NVDA" or company_name.upper() == "NVIDIA" or company_name.upper() == "NVIDA":
                stock_symbol = "NVDA"
            else:
                with st.spinner("Fetching stock symbol..."):
                    stock_symbol = get_stock_symbol(company_name)
            if stock_symbol:
                st.title("Stock Price Visualization App")
                st.write(f"Displaying stock data for {stock_symbol}")

                with st.spinner("Fetching stock data..."):
                    stock_data = get_stock_data(stock_symbol, start_date, end_date)

                if stock_data is not None:
                    plot_stock_data(stock_data)
                    lowest_point = stock_data['Close'].min()
                    highest_point = stock_data['Close'].max()
                    chart_data = pd.DataFrame({
                        'Date': stock_data.index,
                        'Stock Price': stock_data['Close'],
                        'Lowest Point': lowest_point,
                        'Highest Point': highest_point
                    })
                    st.line_chart(chart_data.set_index('Date'))
                    st.success(f"Highest Stock Price: ${round(highest_point, 2)}")
                    st.warning(f"Lowest Stock Price: ${round(lowest_point, 2)}")
                    try:
                        with st.spinner("Performing predictions..."):
                            predicted_value_lr = predict_tomorrows_stock_value_linear_regression(stock_data)
                            predicted_value_lstm = predict_tomorrows_stock_value_lstm(stock_data)
                            time.sleep(1)

                        st.write(f"Approximate tomorrow's stock value (Linear Regression): {predicted_value_lr:.2f}$")
                        st.write(f"Approximate tomorrow's stock value (LSTM): {predicted_value_lstm:.2f}$")

                        with st.expander("💡 What is LSTM?"):
                            display_lstm_info()

                        with st.expander("💡 What is Linear Regression?"):
                            st.write("Linear Regression Simulation:")
                            linear_Regression(stock_data)



                    except:
                        st.warning("Not enough info for an AI approximation, please try an earlier date.")
                    investment(stock_symbol, stock_data)
            else:
                st.warning(f"Stock doesn't exist.\ntry again or check your input.")


def investment(stock_symbol, stock_data):
    st.title("Investment")
    if stock_data is not None:
        value = st.slider("If you were to invest:", min_value=100, max_value=5000, value=100, step=50, key="level1")
        start_price = stock_data['Close'].iloc[0]
        end_price = stock_data['Close'].iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100
        potential_returns = value * (1 + percent_change / 100)
        st.write(f"If you invest {value:.2f}$ in {stock_symbol} from the start of 2022 until today:")
        st.success(
            f"You would have approximately {potential_returns:.2f}$ based on the percentage change of {percent_change:.2f}%.")

    else:
        st.warning(f"Stock doesn't exist.\ntry again or check your input.")


def homepage():
    from israelcities import israeli_cities
    st.title("User Authentication System")

    page = st.sidebar.radio("Navigation", ["Sign Up", "Sign In"])

    if page == "Sign Up":
        st.header("Sign Up")
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")

        st.button('Sign up', on_click=click_button)
        if st.session_state.clicked:
            sign_up(username, password)

    elif page == "Sign In":
        st.header("Sign In")
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")
        st.button('Sign in', on_click=click_button)
        if st.session_state.clicked:
            if sign_in(username, password):
                pass





def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'

    st.header(translate_word("Choose a language"))
    language_options = ['English','Russian' , 'Hebrew']
    st.session_state.chosen_language = st.selectbox("Choose a language", language_options)
    st.session_state.chosen_language = st.session_state.chosen_language[:2].lower()




@st.cache_data
def translate_word(word):
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'  
    translator = Translator()
    translated_word = translator.translate(word, dest=st.session_state.chosen_language).text
    return translated_word



page = st.sidebar.radio(translate_word("Select Page"), [translate_word("Home"), translate_word("Stock Analysis"), translate_word("language chooser")])
if page == translate_word("Home"):
    homepage()
elif page == translate_word("Stock Analysis"):
    stockanalyzer()
elif page == translate_word("language chooser"):
    language_chooser()

