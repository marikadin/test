import sys
from urllib.parse import urlparse, parse_qs
import yfinance as yf
from markanditay import search_results_url,selected_date
from datetime import datetime, timedelta

try:
    start_date = datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")
except ValueError:
    start_date = '2022-01-01'

now = datetime.now()
end_date = now.strftime("%Y-%m-%d")

# Convert start_date and end_date to datetime objects
start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

# Create a list to store the dates
date_list = []

# Loop through the dates and append them to the list
current_date = start_date_obj
while current_date <= end_date_obj:
    date_list.append(current_date.strftime("%d-%m-%Y"))
    current_date += timedelta(days=1)
print(date_list)
def extract_stock_symbol(url):
    global stock_symbol
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    stock_symbol = query_params.get('p', [''])[0]

    try:
        data = yf.download(stock_symbol, start=start_date, end=end_date)
    except:
        sys.exit("Couldn't get info.")

    return data['Open'].tolist()

stock_symbol = extract_stock_symbol(search_results_url)