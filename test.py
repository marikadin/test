from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#from extract_ddata import process_fin_streamers
import sys
#from tkcalendar import Calendar
#from datetime import datetime, timedelta
#from PIL import Image, ImageTk
import streamlit as st
x=""
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

keyword = st.text_input("Enter a string:")

# Button to trigger action
if st.button("Submit"):
    # Display the entered string only when the button is pressed
    st.write("You entered:", keyword)

    # Fetch search results URL using Selenium
    st.write("Fetching...")
    driver = webdriver.Chrome(options=chrome_options)
    website_url = 'https://finance.yahoo.com/'

    try:
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yfin-usr-qry')))
        search_bar.clear()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(3)

        search_results_url = driver.current_url
        x=search_results_url
        # Process the obtained URL as needed
        if search_results_url:
            st.write(f"URL of the search results page for {keyword}: {search_results_url}")
        else:
            st.warning(f"No search results found for {keyword}.")
    except:
        st.error("Error!")
    finally:
        driver.quit()



if x == "https://www.yahoo.com/?err=404&err_url=https%3A%2F%2Ffinance.yahoo.com%2Fresearch%2Freports%2FMS_0P0000061X_AnalystReport_1699903723000%3F.tsrc%3Dfin-srch":
    print("Stock is not in Yahoo database.")
    sys.exit(1)
elif "https://finance.yahoo.com" not in x:
    print("Stock is not in Yahoo database.")
    sys.exit(1)
elif "news" in x:
    print("Not a stock but news: ", x)
    sys.exit(1)
elif "/m/" in x:
    print("Stock is not in Yahoo database.")
    sys.exit(1)
elif "/company/" in x:
    print("A private company: ", x)
    sys.exit(1)
else:
    if x:
        print(f"URL of the search results page for {keyword}: {x}")
        # Call the second script's functionality with the obtained URL
        #from extract_ddata import process_fin_streamers
        #process_fin_streamers(keyword, search_results_url)
    else:
        print(f"No search results found for {keyword}.\n")


