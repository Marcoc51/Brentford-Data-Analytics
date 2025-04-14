from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO

def scrape_tables(url: str, club: str, xpath: str = '', sleep_time: int = 10) -> pd.DataFrame:
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # run in headless mode
    options.add_argument("--disable-gpu")

    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Load the page
    driver.get(url)

    # Give the page some time to fully load
    time.sleep(sleep_time)

    try:
        if club == "Brentford":
            soup = BeautifulSoup(driver.page_source, "html.parser")
            df = pd.read_html(StringIO(str(soup)))
        else:
            table_element = driver.find_element(By.XPATH, xpath)
            table_html = table_element.get_attribute('outerHTML')
            df = pd.read_html(StringIO(table_html))[0]
    except Exception as e:
        return f"Error while scraping: {e}"

    # Always close the browser session
    driver.quit()
    return df
