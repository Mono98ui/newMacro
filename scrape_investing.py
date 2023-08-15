import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as fser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from database import database
from datetime import datetime


def openWebBrowser():
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    webdriver_path="./geckodriver.exe"
    driver = webdriver.Firefox(service=fser(executable_path=webdriver_path), options=options)
    return driver

def standardisePercentage(index, value):
    nbr = float(value.replace("%", ""))
    return round(index * (1.00 + nbr/100.00), 2)

def removeNotations(value):
    return  float(value.replace("M", ""))

def format_data_db(tableName, timestamp, value, country):
    data={
        "table":tableName,
        "timestamp": datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
        "value":value,
        "country": country
    }
    return data



def method_ShowMore(driver, info_link):
    index = 1.00 #valeur arbitraire
    driver.get(info_link[1])
    showMore = driver.find_element(By.ID,info_link[2])
    tableName=info_link[3]
    compter = 0
    list_data = []
    
    while( compter < 42 and showMore.is_displayed() and showMore.is_enabled()):
        showMore.click()
        compter+=1
        time.sleep(0.5)


    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    for iter in soup.tbody.find_all("tr"):
        value = -1000.00 #valeur initial arbitraire
        country = "US"
        timestamp = iter["event_timestamp"]
        textValue = iter.find("span").text
        if "%" in textValue:
            value = standardisePercentage(index, textValue)
            index = value
        elif "M" in textValue:
            value = removeNotations(textValue)
        if textValue.strip():
            data = format_data_db(tableName, timestamp, value, country)
            list_data.append(data)
        
    return list_data

db = database("MacroDB","Test_user","test")
info_links=db.fetch_links()
driver = openWebBrowser()
driver.maximize_window()
for info_link in info_links:

    #if showMore is not empty
    if info_link[2]:
        data = method_ShowMore(driver,info_link)
        print(data)
        #db.insert_value_component(info_link[3], data)
        break

driver.quit()