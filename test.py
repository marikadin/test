import streamlit as st
import webbrowser

def open_website():
    url = "https://www.youtube.com/"
    webbrowser.open(url)

st.title("Website Opener")

if st.button("Open Website"):
    open_website()
