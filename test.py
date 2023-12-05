import streamlit as st
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#from extract_ddata import process_fin_streamers
import sys
def get_search_results_url(url, keyword):
    st.write("Fetching...")
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
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

st.title("Stocks")

# Set the minimum and maximum selectable dates
min_date = datetime.date(2022, 1, 1)
max_date = datetime.date.today()

# Get user input for a date within the specified range, with a default value
selected_date = st.date_input("Select a date", min_value=min_date, max_value=max_date, value=min_date)

# Add a text input for stock name
stock_name = st.text_input("Enter Stock Name")

# Add a button to proceed
if st.button("Proceed"):
    # Check if stock name is provided
    if not stock_name:
        st.warning("You must enter a stock name!")
    else:
        st.success(f"Stock Name '{stock_name}' saved!")

        # Rest of your code
        website_url = 'https://finance.yahoo.com/'  
        try:
            # Combine the date and stock name for a more meaningful search
            formatted_date = selected_date.strftime("%Y-%m-%d")
            search_results_url = get_search_results_url(website_url, f"{stock_name} stock {formatted_date}")
            st.write(search_results_url)
        except:
            st.write("Thanks for trying. See you soon(:")
            sys.exit()

        if "404" in search_results_url:
            st.warning("Stock is not in Yahoo database.")
            sys.exit()
        elif "https://finance.yahoo.com" not in search_results_url:
            st.warning("Stock is not in Yahoo database.")
            sys.exit()
        elif "news" in search_results_url:
            st.warning("Not a stock but news: " + search_results_url)
            sys.exit()
        elif "/m/" in search_results_url:
            st.warning("Stock is not in Yahoo database.")
            sys.exit()
        elif "/company/" in search_results_url:
            st.warning("A private company: " + search_results_url)
            sys.exit()
        else:
            if search_results_url:
                st.success(f"URL of the search results page for {stock_name}: {search_results_url}")
                # Call the second script's functionality with the obtained URL
                #process_fin_streamers(stock_name, search_results_url)
            else:
                st.warning(f"No search results found for {stock_name}.")

# Function to get the search results URL

