#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import re

# Fetch a specific version of ChromeDriver
service = Service(ChromeDriverManager(driver_version="131.0.6778").install())
driver = webdriver.Chrome(service=service)
PATH = "/Users/raoultschudin/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.transfermarkt.ch/")
driver.implicitly_wait(10)
print(driver.title)

iframes = driver.find_elements(By.CSS_SELECTOR,'iframe')
iframe = driver.find_element(By.ID,'sp_message_iframe_953386')
driver.switch_to.frame(iframe)
cookie_element = driver.find_element(By.XPATH, '//*[@id="notice"]/div[3]/div[1]/div[1]/button')
cookie_element.click()
driver.switch_to.default_content()
try:
    search_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Suchbegriff eingeben (Spieler, Verein,...)"]'))
)
    search_field.send_keys("Ruiz")
    search_field.send_keys(Keys.RETURN)
except Exception as e:
    print("Search field not found:", e)
#search = driver.find_element(By.CLASS_NAME, "tm-header__input--search-field")
#search.send_keys("Ruiz")
#search.send_keys(Keys.RETURN)

def get_player_names(page_number):
    page_number += 1
    try:
        element = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                              "#yw0 > div.pager > ul > li.tm-pagination__list-item.tm-pagination__list-item--active"),
                                              str(page_number))
            )
    except:
        print('this is an exception')
        driver.quit()

    table = driver.find_element(By.TAG_NAME, "tbody")
    lines = table.find_elements(By.CLASS_NAME, 'odd' or 'even')
    for line in lines:
        player_and_value = line.find_elements(By.CLASS_NAME, "hauptlink")
        for pandv in player_and_value:
            contains_digit = any(char.isdigit() for char in pandv.text)
            if not contains_digit:
                if not pandv.text.startswith('-'):
                    print('Player_name:', pandv.text)
            else:
                if not pandv.text.startswith('-'):
                    print('Value:', pandv.text)
        several_characteristics_of_player = line.find_elements(By.CLASS_NAME, 'zentriert')
        for characteristic in several_characteristics_of_player:
            if len(characteristic.text) > 0:
                if characteristic.text.isalpha():
                    print('Position:', characteristic.text)
                else:
                    print('Age:', characteristic.text)
        club_and_nationality = line.find_elements(By.TAG_NAME, 'img')
        for candn in club_and_nationality:
            if candn.get_attribute('class') == 'tiny_wappen':
                print('Club:', candn.get_attribute('alt'))
            elif candn.get_attribute('class') == 'flaggenrahmen':
                print('Nationality:', candn.get_attribute('alt'))
    next_page = page_number + 1
    link = driver.find_element(By.LINK_TEXT, str(next_page))
    link.click()
    get_player_names(page_number)

driver.implicitly_wait(10)
get_player_names(0)

time.sleep(5)


driver.quit()


# In[ ]:




