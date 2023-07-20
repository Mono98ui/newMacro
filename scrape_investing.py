import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as fser
from selenium.webdriver.common.keys import Keys
import database


def method_ShowMore(driver):
    showMore = driver.find_element(By.ID,"showMoreHistory70")
    compter = 0
    while( compter < 42):
        showMore.click()
        compter+=1
        time.sleep(1)


    page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    for iter in soup.tbody.find_all("span"):
        print(iter.text)

    for iter in soup.tbody.find_all("tr"):
        print(iter["event_timestamp"])

def method_HistoricalData(driver):
    dateBtn = driver.find_element(By.CLASS_NAME, "DatePickerWrapper_input__UVqms")
    dateBtn.click()
    inputDate = driver.find_elements(By.CSS_SELECTOR,"input[type='date']")[0]
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(inputDate, 5, 5)
    #action.click()
    #action.perform()
    #print(inputDate.get_attribute('outerHTML'))
    #inputDate.clear()
    #inputDate.send_keys("2002-01-01")
    #driver.execute_script("arguments[0].setAttribute('value', arguments[1])", inputDate, "2002-01-01")
    submitBtn = driver.find_element(By.CSS_SELECTOR, "button[class='inv-button HistoryDatePicker_apply-button__Oj7Hu']")
    submitBtn.click()
    time.sleep(5)

URL = "https://ca.investing.com/economic-calendar/us-leading-index-1968"
options = webdriver.FirefoxOptions()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
webdriver_path="./geckodriver.exe"
driver = webdriver.Firefox(service=fser(executable_path=webdriver_path), options=options)
driver.get(URL)

#method_HistoricalData(driver)
method_ShowMore(driver)

driver.quit()