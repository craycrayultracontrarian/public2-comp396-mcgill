# Import dependencies
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.chrome.service import Service

from data.keys.credentials import aws_access_key_id, aws_secret_access_key

from src.aws import upload_to_s3
from src.categorize import categorize_images

def counter():
    with open("junk/sc_counter.txt", "r") as file:
        count = int(file.read())
    with open("junk/sc_counter.txt", "w") as file:
        file.write(str(count + 1))
    return count
global_counter = counter()

left = 575
top = 25
right = 1560
bottom = 1125   

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(r'C:/Users/born2die/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'))

# wait variables
wait5 = WebDriverWait(driver, 5)
wait10 = WebDriverWait(driver, 10)

# open the webpage
driver.get("https://www.instagram.com/")

username = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
# enter username and password
username.clear()
username.send_keys("michealjoneshenny")  # username
password.clear()
password.send_keys("benis1234")  # password
button = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()  # clicking submit button

def click_not_now_button(driver):
    for i in range(5):
        try:
            element_text = "Not now"
            not_now_button = wait10.until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='{element_text}']")))

            not_now_button.click()
            print("[Not now]")
            break
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
            time.sleep(2)

click_not_now_button(driver)

def upload_file():
    upload_to_s3(f'data/screenshots/{global_counter}sc{localcounter}-new.png', 
                 'socialcomputing', 
                 f'ig_reels/{global_counter}sc{localcounter}-new.png', 
                 aws_access_key_id, 
                 aws_secret_access_key)

Not_Now_button = wait10.until(
    EC.element_to_be_clickable((By.CLASS_NAME, '_a9_1'))
)
Not_Now_button.click()
print("Clicked 'Not Now'")

# this method works too
driver.get('https://www.instagram.com/reels/')
print("Opened Reels")

time.sleep(1)

reels = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"]')
localcounter = 0
thumbnails = []
left_profile_list = []
right_profile_list = []
leftover_errorcheck = []
profile_button = None
profile_name = None

#document.querySelector('.xuzhngd').parentElement.parentElement.parentElement.parentElement.querySelector('img[alt*="profile picture" i]')
# in essence we already have the username, but parsing the result from the above selector would be easy too. 
# we will implement and test this: querySelector('img[alt*="profile picture" i]
# the only thing left to see is if clicking the profile picture (now that we have it) works

#click on the profile to get good screenshots
def clicknsave_profile():
    profile_button = parent_div.find_element(By.CSS_SELECTOR, 'img[alt*="profile picture"]')
    print("got profile button")
    user_disorganized = profile_button.get_attribute('alt')
    profile_name = user_disorganized.split(' profile picture')[0]
    print(profile_name)
    profile_button.click()
    print("Arrived at profile")

while True:
    try:
        localcounter+=1
        
        # get current reel
        current_reel = driver.find_element(By.CLASS_NAME, 'xuzhngd')
        print("got current reel")
        # get parent div
        parent_div = current_reel.find_element(By.XPATH, '.. /.. /..')
        print("got parent div")
        
        # Move to the next reel by simulating a down arrow key press
        time.sleep(0.5)
        print("Scrolling down "+str(localcounter))
        reels = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"]')
        reels.send_keys(Keys.ARROW_DOWN)
        

        clicknsave_profile()

        # get screenshot
        time.sleep(5)
        driver.execute_script("document.body.style.zoom='50%'")
        png = driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im = im.crop((left, top, right, bottom))
        im.save('data/screenshots/'+f'{global_counter}sc{localcounter}-new.png')

        thumbnails = [f'https://socialcomputing.s3.amazonaws.com/ig_reels/{global_counter}sc{localcounter}-new.png']
        print (thumbnails)

        time.sleep(1)
        upload_file()

        # Categorize the images using OpenAI's GPT-4o model, checks for errors, and prints
        print(categorize_images(thumbnails))
        result = categorize_images(thumbnails)
        # I will then, depending on what the categorize function returns, either save the username, or not
        if result == 'LEFT':
            left_profile_list += profile_name
            if result == 'RIGHT':
                right_profile_list += profile_name
            else : leftover_errorcheck += profile_name

        print(len(left_profile_list))
        print(len(right_profile_list))
        print(len(leftover_errorcheck))
        # then, I'll return to the reels page
        driver.get('https://www.instagram.com/reels/')
        print("Went back to Reels")

        

    except Exception as e:
        print(f"An error occurred: {e}")
        break

    # current video (the active one)
    # xz74otr x1bs05mj x5yr21d x10l6tqk x1d8287x x19991ni xwzpupj // xuzhngd // 
    # this is the id of our active video which we can use to get attributes

    # future reference: AWS works great but naming convention is weird on AWS 1 10 2 .. 8 9 is the order. so 001 file names may be better 