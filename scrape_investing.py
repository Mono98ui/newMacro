import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as fser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from database import database
import datetime
from datetime import datetime
import os
from private import Private

#
#Param:
#This function open the browser
#
def openWebBrowser():
    options = webdriver.FirefoxOptions()
    #A modifier
    options.binary_location = os.getenv('WEB_DRIVER_PATH')
    webdriver_path="./geckodriver.exe"
    driver = webdriver.Firefox(service=fser(executable_path=webdriver_path), options=options)
    return driver
#
#Param:
#index: arbitrary value calulate from the earlist data
#value: The value of the indicator
#This function standardise the value(percentage) of a indicator
#return: the standardise value
#
def standardisePercentage(index, value):
    nbr = float(value.replace("%", ""))
    return round(index * (1.00 + nbr/100.00), 2)
#
#Param:
#value: The value of the indicator
#This function remove the million notation
#return: the value
#
def removeNotations(value):
    return  float(value.replace("M", ""))
#
#Param:
#timestamp: the date of publication of the data
#value: The value of the indicator
#This function encapsulate the data into a dictionnary
#return: dictionnary
#
def format_data_db(timestamp, value):
    data={
        "timestamp": timestamp,
        "value":value,
    }
    return data


#
#Param:
#driver: the browser driver
#info_link: the info of the module in investing.com
#This function scrape the data of investing.com until 2002-01-01
#return: list of data(value) of a indicator
#
def method_ShowMore(driver, info_link):
    index = 1.00 #valeur arbitraire
    driver.get(info_link[1])
    showMore = driver.find_element(By.ID,info_link[2])
    tableName=info_link[4].strip()
    compter = 0
    list_data = []
    onlyNewestdata = False
    #fix
    compter_fix = 0

    start_date = datetime(2002, 1, 1)
    end_date = datetime.now()

    # Calculate the Total Number of months between two dates
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    print(num_months)

    while( compter <  int(num_months/6)  and showMore.is_displayed() and showMore.is_enabled()):
        showMore.click()
        compter+=1
        time.sleep(0.5)


    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    for iter in reversed(soup.tbody.find_all("tr")):
        value = -1000.00 #valeur initial arbitraire
        timestamp =  datetime.strptime(iter["event_timestamp"], '%Y-%m-%d %H:%M:%S')
        #fix the data
        if timestamp == datetime(2013, 11, 26, 13, 30) and tableName == "t_building_permits_25":
            compter_fix+=1
            if compter_fix > 1:
                timestamp = datetime(2013, 10, 26, 13, 30)

        textValue = iter.find("span").text.replace(",", "")

        #fix the data
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


pr = Private()


db = database(os.getenv('DB_NAME'),os.getenv('DB_USER'),os.getenv('DB_PASSWORD'))
db.update_status("process_investing", 1)
info_links=db.fetch_links()
driver = openWebBrowser()
driver.maximize_window()
print(info_links)
for info_link in info_links:

    #if showMore is not empty
    if info_link[2]:
        try:
            data = method_ShowMore(driver,info_link)
            db.insert_value_component(info_link[4].strip(), data)
        except:
            #Creer des logs
            db.update_status("process_investing", -1)
driver.quit()
db.update_status("process_investing", 2)

pr.clean()