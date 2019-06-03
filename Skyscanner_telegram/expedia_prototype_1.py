# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:04:00 2019

@author: xiangong
"""
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:04:02 2019

@author: xiangong
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import datetime
import smtplib
import datetime
from calendar import monthrange

#Setting origin, destination
origin_country = "Singapore"
destination_country = "Okinawa"
travel_days = 3
travel_month = 9
travel_year = 2019
max_extraction = 5

start_date_str = str(travel_month)+"/01/2019" 
start_date = datetime.datetime(travel_year, travel_month, 1)

end_date = start_date + datetime.timedelta(days=travel_days)

total_days_in_month = monthrange(travel_year, travel_month)[1]
print(start_date.strftime("%d/%m/%Y"))
print(end_date.strftime("%d/%m/%Y"))

#Start selenium
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--incognito")
#driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
driver.get("https://www.expedia.com.sg/")
sleep(1.5)

#switch to flight only
flight_elem = driver.find_element_by_id("tab-flight-tab-hp")
sleep(1)
flight_elem.click()

#Enter input
origin_elem = driver.find_element_by_id("flight-origin-hp-flight")
sleep(1)
origin_elem.clear()
sleep(1)
origin_elem.send_keys(origin_country)
sleep(1)
origin_elem.send_keys(Keys.ENTER)
sleep(1)

destination_elem = driver.find_element_by_id("flight-destination-hp-flight")
sleep(1)
destination_elem.clear()
sleep(1)
destination_elem.send_keys(destination_country)
sleep(1)
destination_elem.send_keys(Keys.ENTER)
sleep(1)

dep_elem = driver.find_element_by_id("flight-departing-hp-flight")
dep_elem.clear()
dep_elem.send_keys(start_date.strftime("%d/%m/%Y"))

arr_elem = driver.find_element_by_id("flight-returning-hp-flight")
for i in range(11):
        arr_elem.send_keys(Keys.BACKSPACE)
arr_elem.send_keys(end_date.strftime("%d/%m/%Y"))

#Search
submit_elem = driver.find_element_by_xpath('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')
submit_elem.click()
sleep(10)

#Create main dataframe
main_df = pd.DataFrame()

#Create dataframe
df = pd.DataFrame()

#Extract info
try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@data-test-id='departure-time']")))
finally:
    pass

#Departure time
dep_times = driver.find_elements_by_xpath("//span[@data-test-id='departure-time']")
dep_times_list = [dep_times[i].text for i in range(max_extraction)]
    
#Arrival time
arr_times = driver.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
arr_times_list = [arr_times[i].text for i in range(max_extraction)]

#airline name
airlines = driver.find_elements_by_xpath("//span[@data-test-id='airline-name']")
airline_list = [airlines[i].text for i in range(max_extraction)]

#Prices
prices = driver.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
price_list = [prices[i].text.split('$')[1] for i in range(max_extraction)]

#durations
durations = driver.find_elements_by_xpath("//span[@data-test-id='duration']")
durations_list = [durations[i].text for i in range(max_extraction)]

#stops
stops = driver.find_elements_by_xpath("//span[@class='number-stops']")
stops_list = [stops[i].text for i in range(max_extraction)]

#layovers
layovers = driver.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
layovers_list = [layovers[i].text for i in range(max_extraction)]

#Return lists
return_dep_list = []
return_arr_list = []
return_airline_list = []
return_price_list = []
return_duration_list = []
return_stops_list = []
return_layovers_list = []

#Obtaining return offer
for i in range(len(dep_times_list)):
    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test-id='select-button']")))
    finally:
        returns = driver.find_elements_by_xpath("//button[@data-test-id='select-button']")
        return_button = returns[i]
        return_button.click()
        sleep(2)
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@data-test-id='listing-price-dollars']")))
        finally:
            #Return departure time
            return_dep_times = driver.find_elements_by_xpath("//span[@data-test-id='departure-time']")
            return_dep_list.append(return_dep_times[0].text)
            
            #Return arrival time
            return_arr_times = driver.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
            return_arr_list.append(return_arr_times[0].text)
            
            #Return airline
            return_airlines = driver.find_elements_by_xpath("//span[@data-test-id='airline-name']")
            return_airline_list.append(return_airlines[0].text)
            
            #Return price
            return_prices = driver.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
            return_price_list.append(return_prices[0].text.split('$')[1])
            
            #Return duration
            return_durations = driver.find_elements_by_xpath("//span[@data-test-id='duration']")
            return_duration_list.append(return_durations[0].text)
            
            #return stop over
            return_stopovers = driver.find_elements_by_xpath("//span[@class='number-stops']")
            return_stops_list.append(return_stopovers[0].text)
            
            #Return layovers
            return_layovers = driver.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
            return_layovers_list.append(return_layovers[0].text)
            driver.back()
            sleep(5)

#Compiling
for i in range(len(dep_times_list)):
    try:
        df.loc[i, 'departure time'] = dep_times_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'arrival time'] = arr_times_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'airline'] = airline_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'price'] = price_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'duration'] = durations_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'stops'] = stops_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'layover'] = layovers_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'return departure time'] = return_dep_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'return arrival time'] = return_arr_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'return airline'] = return_airline_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'return price'] = return_price_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'return duration'] = return_duration_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'return stops'] = return_stops_list[i]
    except Exception as e:
        pass
    try:
        df.loc[i, 'layover'] = return_layovers_list[i]
    except Exception as e:
        pass
    
main_df = pd.concat([main_df, df])

#Next dates
start_date += datetime.timedelta(days=1)
end_date += datetime.timedelta(days=1)

dep_elem = driver.find_element_by_id("departure-date-1")
dep_elem.clear()
dep_elem.send_keys(start_date.strftime("%d/%m/%Y"))

arr_elem = driver.find_element_by_id("return-date-1")
for i in range(11):
        arr_elem.send_keys(Keys.BACKSPACE)
arr_elem.send_keys(end_date.strftime("%d/%m/%Y"))

#Search
submit_elem = driver.find_element_by_id('flight-wizard-search-button')
submit_elem.click()
sleep(10)

#driver.close()
        

        
        
        
        
        
        
        
        
