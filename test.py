import streamlit as st
from other_dates import stock_symbol, date_list
from extract_ddata import values
import sys
from markanditay import keyword


st.title("Stocks")


y = stock_symbol
x = date_list
percent_change = 0

try:
    last_price = values
    if y[-1] != y[-2]:
        percent_change = (y[-1] - y[-2]) / y[-2] * 100
        percent_text = f"The percent of change is: {percent_change:.2f}%"
    else:
        percent_text = "The percent of change is: 0.00%"
except:
    try:
        if y[-1] != y[-2]:
            percent_change = (y[-1] - y[-2]) / y[-2] * 100
            percent_text = f"{percent_change:.2f}%"
    except:
        st.error("An error occurred, try another date.")
        sys.exit()
    else:
        percent_text = "0.00%"

try:
    last_price = f"Today the open value is: ${y[-1]:,.2f}"
except:
    last_price = f"Today the open value is: ${values}"

text_color = "black"
if percent_change > 0:
    text_color = "green"
elif percent_change < 0:
    text_color = "red"


st.text(last_price)
st.text(percent_text)


st.line_chart(y)


