import webbrowser
import time
import streamlit as st
import sys
from bs4 import BeautifulSoup
import requests
def get_search_results_url(url, keyword):
    st.write("Fetching...")

    try:
        # Construct the search URL
        search_url = f"{url}/quote/{keyword}"

        # Use requests to get the HTML content of the page
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the URL of the first search result
        first_result = soup.find('a', {'data-test': 'search-link'})
        if first_result:
            first_result_url = f"{url}{first_result['href']}"
            
            # Open the first result URL in the default web browser
            webbrowser.open_new_tab(first_result_url)

            # Return the first result URL
            return first_result_url
        else:
            st.write("No search results found.")
            return None

    except Exception as e:
        st.write(f"Failed fetching: {e}")
        return None

website_url = 'https://finance.yahoo.com/'  
keyword = st.text_input("Enter the stock name:")



website_url = 'https://finance.yahoo.com/'  
keyword = st.text_input("Enter the stock name:")
if st.button("Enter"):
    try:
        search_results_url = get_search_results_url(website_url, keyword)
    except:
        st.write("Thanks for trying. \nSee u soon(:")
        sys.exit()

    # Rest of the conditions based on the original code
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
            # from extract_ddata import process_fin_streamers
            # process_fin_streamers(keyword, search_results_url)
        else:
            st.write(f"No search results found for {keyword}.\n")
