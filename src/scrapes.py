# Import dependencies
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
import logs
from bs4 import BeautifulSoup
import re
import json
import os
from urllib.parse import urlparse
import csv
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

######################################################################################################
# MUST RUN mitmdump -s logs.py in terminal before running this script ############################
######################################################################################################

with open("../data/logging_client_events/counter.txt", "r") as file:
    count = int(file.read())
with open("../data/logging_client_events/counter.txt", "w") as file:
    file.write(str(count + 1))
print(count)
with open("../data/logging_client_events/counter.txt", "r") as file:
    count_updated = int(file.read())
print(count_updated)

# Setting up
# Set up the proxy to use Mitmproxy
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = '127.0.0.1:8080'
proxy.ssl_proxy = '127.0.0.1:8080'

# Set up Chrome options to use Mitmproxy
chrome_options = Options()
chrome_options.add_argument('--proxy-server=http://127.0.0.1:8080')
chrome_options.add_argument('--headless')  # Enable headless mode
# chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
# chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
# chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

# Initialize the WebDriver with options
driver = webdriver.Chrome(options=chrome_options)

# wait variables
wait5 = WebDriverWait(driver, 5)
wait10 = WebDriverWait(driver, 10)
wait2 = WebDriverWait(driver, 2)

######################################################################################################
# open the webpage
driver.get("https://www.instagram.com/")

username = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
# enter username and password
username.clear()
username.send_keys("minesweeper_enthusiast")  # username
password.clear()
password.send_keys("marco1231$")  # password
button = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()  # clicking submit button

# Function to safely find an element with retries
def find_element_with_retries(by, value, retries=5):
    for _ in range(retries):
        try:
            return driver.find_element(by, value)
        except (StaleElementReferenceException, NoSuchElementException):
            pass
    return None
# Logged in now

# click on not now buttons
def click_not_now_button(driver, retries=5):
    for i in range(retries):
        try:
            # Wait for the "Not Now" button to be clickable
            not_now_button = wait10.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div'))
            )
            # Click the "Not Now" button using JavaScript
            driver.execute_script("arguments[0].click();", not_now_button)
            print("Clicked 'not now' button")
            break
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying


click_not_now_button(driver)

# click on not now button
Not_Now_button = wait10.until(
    EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'))
)
Not_Now_button.click()
print("Clicked 'Not Now'")

# click on reels
# search_button = WebDriverWait(driver, 5).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[aria-label="Reels"]')))
# search_button.click()

# this method works too
driver.get('https://www.instagram.com/reels/')
print("Opened Reels")

######################################################################################################
# Now in REELS

debug_counter = 0
def scroll():
    global debug_counter
    reels = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"]')

    # debug
    debug_counter += 1
    print("Scrolling down " + str(debug_counter))
    reels.send_keys(Keys.ARROW_DOWN)

def get_like_button(current_reel):
    # get parent div
    parent_div = current_reel.find_element(By.XPATH, '.. /.. /..')
    print("got parent div")
    # get like button
    like_button = parent_div.find_element(By.CSS_SELECTOR, 'svg[aria-label="Like"]')
    print("got like button")
    return like_button

while True:
    try:
        time.sleep(4)

        # get current reel
        current_reel = driver.find_element(By.CLASS_NAME, 'xuzhngd')
        print("got current reel")


        ############################## LIKE ########################################
        like_button = get_like_button(current_reel)
        like_button.click()
        print("Liked the reel")

        ############################## LIKE COUNT ##################################
        # Move up to the desired parent element
        desired_parent = like_button.find_element(By.XPATH, "./ancestor::div[5]")
        print("Got desired parent")
        print(desired_parent.get_attribute("class"))
        # Navigate back down to the like count element
        like_count_element = desired_parent.find_element(By.XPATH,
                                                         ".//div[@role='button']/div[@class='html-div']/div[@class='html-div']/span[@dir='auto']/span[@class='html-span']")

        # Get the text of the like count
        like_count = like_count_element.text

        # Print the like count
        print(f"Like count: {like_count}")





        # #################################
        time.sleep(1)

        scroll()






    except Exception as e:
        print(f"An error occurred: {e}")
        break
