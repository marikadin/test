import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# Specify the path to your Chrome executable
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"  

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.binary_location = chrome_path

st.title("Stocks")

# Streamlit widgets for user input
keyword = st.text_input("Enter the stock name:")
selected_date = st.date_input("Select Date", min_value=datetime(2022, 1, 1), max_value=datetime.now())

# Streamlit button to trigger the search
if st.button("Search"):
    st.write("Fetching...")
    
    def get_search_results_url(url, keyword):
        driver = webdriver.Chrome(executable_path="path/to/chromedriver", options=chrome_options)
        driver.get(url)

        try:
            search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yfin-usr-qry')))
            search_bar.clear()
            search_bar.send_keys(keyword)
            search_bar.send_keys(Keys.RETURN)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            time.sleep(3)
            search_results_url = driver.current_url
            return search_results_url

        finally:
            driver.quit()

    website_url = 'https://finance.yahoo.com/'
    try:
        search_results_url = get_search_results_url(website_url, keyword)
    except:
        st.write("Thanks for trying. See you soon(:")
        st.stop()
    finally:
        if not search_results_url:
            st.write("No search results found.")
        elif "https://www.yahoo.com/?err=404&err_url=" in search_results_url:
            st.write("Stock is not in Yahoo database.")
        elif "https://finance.yahoo.com" not in search_results_url:
            st.write("Stock is not in Yahoo database.")
        elif "news" in search_results_url:
            st.write("Not a stock but news:", search_results_url)
        elif "/m/" in search_results_url:
            st.write("Stock is not in Yahoo database.")
        elif "/company/" in search_results_url:
            st.write("A private company:", search_results_url)
        else:
            st.write(f"URL of the search results page for {keyword}: {search_results_url}")
            print(f"Value of search_results_url: {search_results_url}")  