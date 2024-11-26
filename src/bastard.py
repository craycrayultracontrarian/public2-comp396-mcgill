# Import dependencies
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
import time
import random

from selenium.webdriver.common.action_chains import ActionChains

from data.keys.credentials import aws_access_key_id, aws_secret_access_key

from src.download import download_image
from src.aws import upload_to_s3
from src.categorize import categorize_images

def counter():
    with open("junk/sc_counter.txt", "r") as file:
        count = int(file.read())
    with open("junk/sc_counter.txt", "w") as file:
        file.write(str(count + 1))
    return count
global_counter = counter()

left = 745
top = 70
right = 1295
bottom = 1048

# Initialize the WebDriver
driver = webdriver.Chrome()

# wait variables
wait5 = WebDriverWait(driver, 5)
wait10 = WebDriverWait(driver, 10)

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

def upload_file(number):
    upload_to_s3(f'data/screenshots/{global_counter}sc{localcounter}-{number}.png', 
                 'socialcomputing', 
                 f'ig_reels/{global_counter}sc{localcounter}-{number}.png', 
                 aws_access_key_id, 
                 aws_secret_access_key)

Not_Now_button = wait10.until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'))
)
Not_Now_button.click()
print("Clicked 'Not Now'")

# this method works too
driver.get('https://www.instagram.com/reels/')
print("Opened Reels")

time.sleep(1)

reels = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"]')
localcounter = 0
while True:
    try:
        
        # # Initialize a list to hold file paths and S3 keys, clear it out every iteration
        # localcounter+=1
        # numbers = []
        # thumbnails = []
        
        # # get t+0.5 screenshot
        # time.sleep(0.5)
        # png = driver.get_screenshot_as_png()
        # im = Image.open(BytesIO(png))
        # im = im.crop((left, top, right, bottom))
        # im.save('data/screenshots/'+f'{global_counter}sc{localcounter}-2.png')

        # # get t+1 screenshot
        # time.sleep(0.5)
        # png = driver.get_screenshot_as_png()
        # im = Image.open(BytesIO(png))
        # im = im.crop((left, top, right, bottom))
        # im.save('data/screenshots/'+f'{global_counter}sc{localcounter}-3.png')
        
        # # get thumnail and download
        # current_thumbnail = driver.find_element(By.CSS_SELECTOR, 'img[class="xz74otr x1bs05mj x5yr21d x10l6tqk x1d8287x x19991ni xwzpupj xuzhngd"]')
        # link = current_thumbnail.get_attribute('src')
        # download_image(link, 'data/screenshots/', f'{global_counter}sc{localcounter}-1.png')

        # numbers = [1, 2, 3]
        # thumbnails = [f'https://socialcomputing.s3.amazonaws.com/ig_reels/{global_counter}sc{localcounter}-{number}.png' for number in numbers]
        # print (thumbnails)

        # with ThreadPoolExecutor(max_workers=3) as executor:
        #     futures = [executor.submit(upload_file, number) for number in numbers]
        
        # # Categorize the images using OpenAI's GPT-4o model, checks for errors, and prints
        # categorize_images(thumbnails)
        # # we have now enabled the classification of the images in real time
        # # and we'll be able to take actions based on this classification, such as a 'like'

        # # all that's left is to implement these functions based on the classification
        # # first we'll make the function before implementing a simple 'if then' to use them
        # **/
        # get current reel for our functions to act on
        current_reel = driver.find_element(By.CLASS_NAME, 'xuzhngd')
        print("got current reel")
        # get parent div
        parent_div = current_reel.find_element(By.XPATH, '.. /.. /..')
        print("got parent div")

        # def like_post():
        #     try:
        #         # Wait for the SVG element with aria-label="Like" to be present
        #         like_button = WebDriverWait(parent_div, 10).until(
        #             EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Like"]'))
        #         )
        #         print("Got like button")

        #         # Scroll into view
        #         driver.execute_script("arguments[0].scrollIntoView(true);", like_button)

        #         # Wait for the element to be clickable
        #         like_button = WebDriverWait(parent_div, 10).until(
        #             EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[aria-label="Like"]'))
        #         )

        #         # Check if the element is still in a valid state
        #         if like_button.is_displayed() and like_button.is_enabled():
        #             # Use JavaScript to click the element
        #             driver.execute_script("arguments[0].click();", like_button)
        #             print("Liked the reel")
        #         else:
        #             print("Element is obscured or not clickable")
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        
        def save_post():
            save_button = parent_div.find_element(By.CSS_SELECTOR, 'svg[aria-label="Save"]')
            print("got save button")
            save_button.click()
            print("Saved the reel")
        
        def follow_user():
            follow_button = parent_div.find_element(By.XPATH, "//div[text()='Follow']")
            print("got follow button")
            follow_button.click()
            print("Followed the user")
        
        def generate_random_comment():
            comments = [
                "Awesome video! Loved it!",
                "This is exactly what I needed to see today!",
                "Amazing content as always!",
                "Love this video! Keep it up!",
                "So insightful and well-made!",
                "Thanks for the inspiration!",
                "Totally agree with this!",
                "Fantastic video! Learned a lot.",
                "Your videos always make my day!",
                "Great perspective! Thanks for sharing!"
            ]
            return random.choice(comments)
    
        def comment_on_reel():
            comment_button = parent_div.find_element(By.CSS_SELECTOR, 'svg[aria-label="Comment"]')
            comment_button.click()
            print("Clicked comment button")
            time.sleep(3)
            textbox =  wait10.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Add a comment…']")))
            textbox =  wait10.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Add a comment…']")))
            textbox.click()
            driver.switch_to.active_element.send_keys(generate_random_comment())
            driver.switch_to.active_element.send_keys(Keys.ENTER)
            print("Commented on the reel")

        # Like, save, follow, and comment on the reel
        
        # like_post() # doesnt work
        # time.sleep(5)
        save_post()
        time.sleep(5)
        follow_user()
        time.sleep(5)
        comment_on_reel()
        time.sleep(5)
        
        # Move to the next reel by simulating a down arrow key press
        time.sleep(0.5)
        print("Scrolling down "+str(localcounter))
        reels.send_keys(Keys.ARROW_DOWN)
        # works great but naming convention is weird on AWS 1 10 2 .. 8 9 is the order. so 001 file names may be better 
        

    except Exception as e:
        print(f"An error occurred: {e}")
        break

    # current video (the active one)
    # xz74otr x1bs05mj x5yr21d x10l6tqk x1d8287x x19991ni xwzpupj // xuzhngd // 
    # this is the id of our active video which we can use to get attributes


    

    