import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as fser
from database import database
from datetime import datetime
import os
from private import Private
from round_decimal import round_decimal
import logging

# Set up logging
LOG_FILE = "transformation_log.txt"
PREV_LOG_FILE = "prev_transformation_log.txt"

# Remove or archive the old log file if it exists
if os.path.exists(LOG_FILE):
    if os.path.isfile(PREV_LOG_FILE):
        os.remove(PREV_LOG_FILE)
    os.rename(LOG_FILE, PREV_LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to log transformations
def log_transformation(indicator_name, message):
    logging.info(f"[{indicator_name}] {message}")

# Open the browser and return the driver instance
def open_web_browser():
    options = webdriver.FirefoxOptions()
    options.binary_location = os.getenv('WEB_DRIVER_PATH')
    webdriver_path = "./geckodriver.exe"
    return webdriver.Firefox(service=fser(executable_path=webdriver_path), options=options)

# Remove percentage sign and standardize value
def remove_percentage(value):
    return round_decimal(value.replace("%", ""))

# Remove million notation and standardize value
def remove_notations(value):
    return round_decimal(value.replace("M", ""))

# Format data for database insertion
def format_data_db(timestamp, value):
    return {
        "timestamp": timestamp,
        "value": value,
    }

# Scrape data from investing.com until 2002-01-01
def method_show_more(info_link):
    driver = open_web_browser()
    driver.maximize_window()

    # Navigate to the link
    driver.execute_script(f"location.href='{info_link[1]}';")
    time.sleep(5)

    show_more = driver.find_element(By.ID, info_link[2])
    table_name = info_link[4].strip()
    list_data = []
    compter_fix = 0

    start_date = datetime(2002, 1, 1)
    end_date = datetime.now()

    # Calculate the total number of months between start and end dates
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    # Click "Show More" until the data is fully loaded or limit is reached
    for _ in range(num_months // 6):
        if show_more.is_displayed() and show_more.is_enabled():
            show_more.click()
            time.sleep(1)
        else:
            break

    # Parse the page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for row in reversed(soup.tbody.find_all("tr")):
        value = round_decimal(-1000)  # Initial arbitrary value
        timestamp = datetime.strptime(row["event_timestamp"], '%Y-%m-%d %H:%M:%S')

        # Fix specific data issues
        if timestamp == datetime(2013, 11, 26, 13, 30) and table_name == "t_building_permits_25":
            compter_fix += 1
            if compter_fix > 1:
                timestamp = datetime(2013, 10, 26, 13, 30)

        text_value = row.find("span").text.replace(",", "")

        if timestamp == datetime(1993, 2, 1, 9, 0) and table_name == "t_total_vehicle_sales_85":
            text_value = "13.22M"

        # Standardize the value based on its format
        if "%" in text_value:
            log_transformation(table_name, f"Before transformation (%): textValue = {text_value}, timestamp={timestamp}")
            value = remove_percentage(text_value)
            log_transformation(table_name, f"After transformation (%): value = {value}, timestamp={timestamp}")
        elif "M" in text_value:
            log_transformation(table_name, f"Before transformation (M): textValue = {text_value}, timestamp={timestamp}")
            value = remove_notations(text_value)
            log_transformation(table_name, f"After transformation (M): value = {value}, timestamp={timestamp}")
        elif text_value.strip():
            log_transformation(table_name, f"Before transformation (general): textValue = {text_value}, timestamp={timestamp}")
            value = round_decimal(text_value)
            log_transformation(table_name, f"After transformation (general): value = {value}, timestamp={timestamp}")

        if text_value.strip():
            list_data.append(format_data_db(timestamp, value))

    driver.quit()
    return list_data

# Main process
pr = Private()
db = database(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

db.update_status("process_investing", 1)
info_links = db.fetch_links()

for info_link in info_links:
    if info_link[2]:
        try:
            print(info_link)
            data = method_show_more(info_link)
            db.insert_value_component(info_link[4].strip(), data)
        except Exception as e:
            print(f"Error: {e}")
            db.update_status("process_investing", -1)
            break

db.update_status("process_investing", 2)

pr.clean()
