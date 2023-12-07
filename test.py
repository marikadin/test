import streamlit as st
import webbrowser

def open_website(url):
    webbrowser.open(url, new=2)
    iframe_code = f'<iframe src="{url}" width="100%" height="600" frameborder="0" scrolling="yes"></iframe>'
    st.markdown(iframe_code, unsafe_allow_html=True)

st.title("Website Viewer")

url_to_open = "https://finance.yahoo.com/"

if st.button("Open Website"):
    open_website(url_to_open)
