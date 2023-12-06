import webbrowser
import time
import streamlit as st
import sys
def get_search_results_url(url, keyword):
    st.write("Fetching...")

    try:
        # Construct the search URL
        search_url = f"{url}/quote/{keyword}"

        # Open the search URL in the default web browser
        webbrowser.open_new_tab(search_url)

        # Sleep for 3 seconds (similar to time.sleep(3) in your original code)
        time.sleep(3)

        # Return the search URL (optional, you can modify this based on your needs)
        return search_url
    except:
        st.write("Failed fetching")
        return None

website_url = 'https://finance.yahoo.com/'  
keyword = st.text_input("Enter the stock name:")

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
