import streamlit as st
from streamlit.components.v1 import html

def open_website(url):
    iframe_code = f'<iframe src="{url}" width="100%" height="600" frameborder="0" scrolling="yes"></iframe>'
    html(iframe_code, height=600)

st.title("Website Viewer")

url_to_open = "https://finance.yahoo.com/"

if st.button("Open Website"):
    open_website(url_to_open)
