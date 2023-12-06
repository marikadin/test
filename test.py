import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

def get_search_results_url(keyword):
    website_url = 'https://finance.yahoo.com/'

    print("Fetching...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(website_url)

    try:
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yfin-usr-qry')))
        search_bar.clear()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(3)

        search_results_url = driver.current_url

        # Check if the URL is valid
        if "https://finance.yahoo.com" not in search_results_url:
            return None  # Invalid URL

        # Check for specific conditions
        if "news" in search_results_url:
            return None  # Not a stock, but news

        return search_results_url

    finally:
        driver.quit()

# Set up Streamlit page
st.set_page_config(page_title="Stocks", page_icon=None, layout='wide')

# Title
st.title("Stocks")

# User Input for Stock Name
keyword = st.text_input("Enter the stock name:")

# Button to Trigger Search
if st.button("Search"):
    if not keyword:
        st.error("Please enter a stock name.")
    else:
        # Process the stock data
        st.write(f"Searching for: {keyword}")

        # Fetch search results URL using Selenium
        search_results_url = get_search_results_url(keyword)

        if search_results_url:
            st.write(f"Search results URL: {search_results_url}")
        else:
            st.warning(f"No valid search results found for {keyword}.")

# Close Button
if st.button("Close"):
    st.stop()  # Stops the Streamlit app
