import streamlit as st

def open_website(url):
    st.components.iframe(url, height=600, scrolling=True)

st.title("Website Viewer")

url_to_open = "https://www.example.com"

if st.button("Open Website"):
    open_website(url_to_open)
