import streamlit as st
#from extract_ddata import process_fin_streamers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def get_search_results_url(url, keyword):
    print("Fetching...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    driver = webdriver.Chrome(options=chrome_options)
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

# Set up Streamlit page
st.set_page_config(page_title="Stocks", page_icon=None, layout='wide')

# Title
st.title("Stocks")

# User Input for Stock Name
keyword = st.text_input("Enter the stock name:")

# Streamlit Calendar
selected_date = st.date_input("Select Date", min_value=datetime(2022, 1, 1), max_value=datetime.now())

# Button to Trigger Update
if st.button("Search"):
    if not keyword:
        st.error("Please enter a stock name.")
    else:
        # Process the stock data
        st.write(f"Search Result: {keyword}")

        # Your logic for processing the data, use keyword and selected_date as needed
        website_url = 'https://finance.yahoo.com/'
        try:
            search_results_url = get_search_results_url(website_url, keyword)
        except:
            st.error("An error occurred while fetching data.")
            st.stop()

        if search_results_url:
            st.write(f"URL of the search results page for {keyword}: {search_results_url}")
            # Call the second script's functionality with the obtained URL
            #process_fin_streamers(keyword, search_results_url)
        else:
            st.warning(f"No search results found for {keyword}.")

# Close Button
if st.button("Close"):
    st.stop()  # Stops the Streamlit app
