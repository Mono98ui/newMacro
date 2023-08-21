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
    #A modifier
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    webdriver_path="./geckodriver.exe"
    driver = webdriver.Firefox(service=fser(executable_path=webdriver_path), options=options)
    return driver

def standardisePercentage(index, value):
    nbr = float(value.replace("%", ""))
    return round(index * (1.00 + nbr/100.00), 2)

def removeNotations(value):
    return  float(value.replace("M", ""))

def format_data_db(timestamp, value):
    data={
        "timestamp": timestamp,
        "value":value,
    }
    return data



def method_ShowMore(driver, info_link):
    index = 1.00 #valeur arbitraire
    driver.get(info_link[1])
    showMore = driver.find_element(By.ID,info_link[2])
    tableName=info_link[4].strip()
    compter = 0
    list_data = []
    #fix
    compter_fix = 0;
    
    while( compter < 42 and showMore.is_displayed() and showMore.is_enabled()):
        showMore.click()
        compter+=1
        time.sleep(0.2)


    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    for iter in reversed(soup.tbody.find_all("tr")):
        value = -1000.00 #valeur initial arbitraire
        timestamp =  datetime.strptime(iter["event_timestamp"], '%Y-%m-%d %H:%M:%S')
        #fix les donnees
        if timestamp == datetime(2013, 11, 26, 13, 30) and tableName == "t_building_permits_25":
            compter_fix+=1
            if compter_fix > 1:
                timestamp = datetime(2013, 10, 26, 13, 30)

        textValue = iter.find("span").text.replace(",", "")

        #fix les donnees
        if timestamp == datetime(1993, 2, 1, 9, 0) and tableName == "t_total_vehicle_sales_85":
            textValue = "13.22M"


        if "%" in textValue:
            value = standardisePercentage(index, textValue)
            index = value
        elif "M" in textValue:
            value = removeNotations(textValue)
        elif textValue.strip():
            value = float(textValue)

        if textValue.strip():
            data = format_data_db(timestamp, value)
            list_data.append(data)
        
    return list_data

def method_ShowMore_Newest(driver, info_link):

    index = 1.00 #valeur arbitraire
    driver.get(info_link[1])
    list_data = []
    
    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")
    iter = soup.tbody.find("tr")
    value = -1000.00 #valeur initial arbitraire
    timestamp =  datetime.strptime(iter["event_timestamp"], '%Y-%m-%d %H:%M:%S')
    textValue = iter.find("span").text.replace(",", "")

    if "%" in textValue:
        value = standardisePercentage(index, textValue)
        index = value
    elif "M" in textValue:
        value = removeNotations(textValue)
    elif textValue.strip():
        value = float(textValue)

    if textValue.strip():
        data = format_data_db(timestamp, value)
        list_data.append(data)
        
    return list_data

db = database("MacroDB","Test_user","test")
db.update_status("process_investing", 1)
info_links=db.fetch_links()
driver = openWebBrowser()
driver.maximize_window()
for info_link in info_links:

    #if showMore is not empty
    if info_link[2]:
        try:
            data = method_ShowMore(driver,info_link)
            #data = method_ShowMore_Newest(driver,info_link)
            db.insert_value_component(info_link[4].strip(), data)
        except:
            #Creer des logs
            db.update_status("process_investing", -1)
driver.quit()
db.update_status("process_investing", 2)