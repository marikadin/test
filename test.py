import streamlit as st
import webbrowser

def main():
    st.title("Yahoo Finance Viewer")

    # Button to open Yahoo Finance
    if st.button("Open Yahoo Finance"):
        url = "https://finance.yahoo.com/"
        webbrowser.open_new_tab(url)

if __name__ == "__main__":
    main()
