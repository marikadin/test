import streamlit as st
import os

# Set proxy environment variables if needed
# Uncomment and replace with actual proxy addresses if required

os.environ['HTTPS_PROXY'] = 'https://inance.yahoo.com/'

def open_website(url):
    iframe_code = f'<iframe src="{url}" width="100%" height="600" frameborder="0" scrolling="yes"></iframe>'
    st.markdown(iframe_code, unsafe_allow_html=True)

st.title("Website Viewer")

url_to_open = "https://finance.yahoo.com/"

if st.button("Open Website"):
    open_website(url_to_open)
