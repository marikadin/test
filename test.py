import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Adjust this path
chrome_driver_path = 'C:\Program Files\Google'  # Adjust this path

def get_chromedriver_version(chrome_driver_path):
    try:
        # Run ChromeDriver with the --version flag
        import subprocess
        result = subprocess.run([chrome_driver_path, '--version'], capture_output=True, text=True)
        chromedriver_version = result.stdout.strip()
        return chromedriver_version
    except Exception as e:
        return f"Error getting ChromeDriver version: {e}"

# Print ChromeDriver version for debugging
chrome_driver_version = get_chromedriver_version(chrome_driver_path)
st.write(f"ChromeDriver version: {chrome_driver_version}")
