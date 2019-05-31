# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:59:12 2019

@author: xiangong
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#inputs
origin_country = "Singapore"
destination_country = "Okinawa"
month_country = "September"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.skyscanner.com.sg/")

time.sleep(5)
#Input the original country
origin_elem = driver.find_element_by_id('fsc-origin-search')
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'fsc-origin-search'))
    )
finally:
    origin_elem.clear()
    origin_elem.send_keys(origin_country)
    origin_elem.send_keys(Keys.RETURN)

time.sleep(5)
#Input the destination
destination_elem = driver.find_element_by_id('fsc-destination-search')
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'fsc-destination-search'))
    )
finally:
    destination_elem.clear()
    destination_elem.send_keys(destination_country)
    destination_elem.send_keys(Keys.RETURN)

time.sleep(5)
#Month selection
date_picker_elem = driver.find_element_by_id('depart-fsc-datepicker-button')
date_picker_elem.send_keys(Keys.ENTER)
month_elem = driver.find_element_by_xpath('//*[@id="depart-fsc-datepicker-popover"]/div/div/div[1]/div/nav/ul/li[2]/button')
month_elem.send_keys(Keys.ENTER)

time.sleep(5)
all_month_elem = driver.find_elements_by_class_name("Monthselector_monthselector__month__3I0Yp")
for months in all_month_elem:
    if month_country in months.text:
        print(months.text)
        months.send_keys(Keys.ENTER)
        break
        
#Next page
next_page_elem = driver.find_element_by_xpath('//*[@id="flights-search-controls-root"]/div/div/form/div[3]/button')
next_page_elem.send_keys(Keys.RETURN)
print("continung")

#time.sleep(3)   

#driver.close()