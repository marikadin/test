import streamlit as st
import webbrowser

def open_website(url):
    webbrowser.open(url, new=2)

st.title("Website Viewer")

url_to_open = "https://finance.yahoo.com/"

if st.button("Open Website"):
    open_website(url_to_open)
