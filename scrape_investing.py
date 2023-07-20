import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as fser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from database import database

def openWebBrowser():
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    webdriver_path="./geckodriver.exe"
    driver = webdriver.Firefox(service=fser(executable_path=webdriver_path), options=options)
    return driver

def method_ShowMore(driver, info_link):
    driver.get(info_link[1])
    showMore = driver.find_element(By.ID,info_link[2])
    compter = 0
    
    while( compter < 42 and showMore.is_displayed() and showMore.is_enabled()):
        showMore.click()
        compter+=1
        time.sleep(1)


    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    for iter in soup.tbody.find_all("span"):
        print(iter.text)

    for iter in soup.tbody.find_all("tr"):
        print(iter["event_timestamp"])

def method_HistoricalData(driver, link):
    driver.get(link)
    dateBtn = driver.find_element(By.CLASS_NAME, "DatePickerWrapper_input__UVqms")
    dateBtn.click()
    inputDate = driver.find_elements(By.CSS_SELECTOR,"input[type='date'][max='2023-07-20']")[0]
    ActionChains(driver).scroll_by_amount(0, 600).perform()
    ActionChains(driver).move_to_element_with_offset(inputDate,0, 44).perform()

    #print(inputDate.get_attribute('outerHTML'))
    #inputDate.clear()
    #inputDate.send_keys("2002-01-01")
    #driver.execute_script("arguments[0].setAttribute('value', arguments[1])", inputDate, "2002-01-01")
    #submitBtn = driver.find_element(By.CSS_SELECTOR, "button[class='inv-button HistoryDatePicker_apply-button__Oj7Hu']")
    #submitBtn.click()
    time.sleep(5)



#db = database("MacroDB","Test_user","test")
#info_links=db.fetch_links()
driver = openWebBrowser()
driver.maximize_window()
method_HistoricalData(driver, "https://ca.investing.com/commodities/copper-historical-data")
#for info_link in info_links:
#    if info_link[2]:
#        method_ShowMore(driver,info_link)

driver.quit()