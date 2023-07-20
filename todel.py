from selenium import webdriver
from selenium.webdriver.firefox.service import Service as fser
  
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains
  
# create webdriver object
options = webdriver.FirefoxOptions()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
webdriver_path="./geckodriver.exe"
driver = webdriver.Firefox(service=fser(executable_path=webdriver_path), options=options)

# get geeksforgeeks.org
driver.get("https://www.geeksforgeeks.org/")
  
# get  element 
element = driver.find_element_by_link_text("Courses")
  
# create action chain object
action = ActionChains(driver)
  
# perform the operation
action.move_to_element_with_offset(element, 100, 200).click().perform()