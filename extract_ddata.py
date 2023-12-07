import markanditay
import sys
import requests
from bs4 import BeautifulSoup
import re
values = ""

def process_fin_streamers(keyword, url):

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        fin_streamers = soup.find_all('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)')

        for fin_streamer in fin_streamers:
            value_match = re.search(r'value="([^"]*)"', str(fin_streamer))
            if value_match:
                value = float(value_match.group(1))
                print("Stock's value is: ",value)
                values = value
                
                return values
                
    else:
        print(f"Failed to fetch the website. Status code: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    keyword = sys.argv[1]
    search_results_url = sys.argv[2]

    process_fin_streamers(keyword, search_results_url)
