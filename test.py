from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
#from extract_ddata import process_fin_streamers
import sys
from tkcalendar import Calendar
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import streamlit as st

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
selected_date = ''
app = tk.Tk()

#background_image_path = r"C:\Users\user\Desktop\פרוייקט י3\הורדה (7).jpg"
#background_image = Image.open(background_image_path)
#background_image = ImageTk.PhotoImage(background_image)

#canvas = tk.Canvas(app, width=app.winfo_screenwidth(), height=app.winfo_screenheight())
#canvas.pack(fill="both", expand=True)
#canvas.create_image(0, 0, anchor="nw", image=background_image)

app.attributes('-fullscreen', True)

app.title("Stocks")

def Update():
    try:
        update_label()
        app.destroy()
    except:
        st.write("You have to type stock name!")

def update_search(event):
    global keyword
    keyword = search_text.get()
    search_entry.delete(0, tk.END)
    search_entry.insert(0, keyword)

def open_calendar():
    top = tk.Toplevel(app)

    min_date = datetime(2022, 1, 1)

    max_date = datetime.now().date()

    cal = Calendar(
        top,
        font="Arial 14",
        selectmode='day',
        locale='en_US',
        cursor="hand1",
        year=max_date.year,
        month=max_date.month,
        day=max_date.day,
        mindate=min_date,
        maxdate=max_date,
    )

    def set_date():
        global selected_date
        try:
            selected_date = str(cal.get_date())
        except:
            selected_date = "2022-01-01"
        search_entry.delete(0, tk.END)
        top.destroy()

    confirm_button = tk.Button(top, text="Select Date", command=set_date)
    confirm_button.pack(pady=10)
    cal.pack()

search_text = tk.StringVar()
search_entry = tk.Entry(app, textvariable=search_text, width=200)
search_entry.pack(pady=10)
search_entry.place(relx=0.5, rely=0.3, anchor="center")
search_entry.bind("<KeyRelease>", update_search)

result_label = tk.Label(app, text="Enter the stock name: ")
result_label.pack(pady=10)
result_label.place(relx=0.5, rely=0.25, anchor="center")




def update_label():
    result_label.config(text="Search Result: " + keyword)

update_button = tk.Button(app, text="Search", command=Update)
update_button.pack(pady=10)
update_button.place(relx=0.5, rely=0.4, anchor="center")

calendar_button = tk.Button(app, text="Select Date", command=open_calendar)
calendar_button.pack(pady=10)
calendar_button.place(relx=0.5, rely=0.5, anchor="center")

close_button = tk.Button(app, text="Close", command=app.destroy, bg='lightcoral', activebackground='red',width=20)
close_button.pack(pady=10)
close_button.place(relx=0.92, rely=0.02, anchor="center")

app.mainloop()


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

website_url = 'https://finance.yahoo.com/'  
try:
    search_results_url = get_search_results_url(website_url, keyword)
except:
    st.write("Thanks for trying. \nSee u soon(:")
    sys.exit()
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


