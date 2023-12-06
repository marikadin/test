from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import keyword
#from extract_ddata import process_fin_streamers
import sys
#from tkcalendar import Calendar
#from datetime import datetime, timedelta
#from PIL import Image, ImageTk
import streamlit as st

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')





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
    except:
        st.write("failed fetching")
    finally:
        driver.quit()

website_url = 'https://finance.yahoo.com/'  

search_results_url = get_search_results_url(website_url, keyword)

if search_results_url == "https://www.yahoo.com/?err=404&err_url=https%3A%2F%2Ffinance.yahoo.com%2Fresearch%2Freports%2FMS_0P0000061X_AnalystReport_1699903723000%3F.tsrc%3Dfin-srch":
    st.write("Stock is not in Yahoo database.")
    sys.exit(1)
elif "https://finance.yahoo.com" not in search_results_url:
    st.write("Stock is not in Yahoo database.")
    sys.exit(1)
elif "news" in search_results_url:
    st.write("Not a stock but news: ", search_results_url)
    sys.exit(1)
elif "/m/" in search_results_url:
    st.write("Stock is not in Yahoo database.")
    sys.exit(1)
elif "/company/" in search_results_url:
    st.write("A private company: ", search_results_url)
    sys.exit(1)
else:
    if search_results_url:
        st.write(f"URL of the search results page for {keyword}: {search_results_url}")
        # Call the second script's functionality with the obtained URL
        #from extract_ddata import process_fin_streamers
        #process_fin_streamers(keyword, search_results_url)
    else:
        st.write(f"No search results found for {keyword}.\n")


