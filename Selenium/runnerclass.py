from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time
import random


class chromedriver():
    def driver(self):
        # PATH to chromedriver.exe
        PATH = "C:\\Users\\kurty\\OneDrive\\Documents\\Python\\Selenium\\chromedriver.exe"

        # incognito mode
        incog = webdriver.ChromeOptions()
        incog.add_argument("--incognito")

        return incog

# Checking runtime
loop_time = time.time()

# Opening the driver in selenium in incog mode
driver = webdriver.Chrome(PATH, options=incog)
driver.maximize_window()

# Switching user agents
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(useragents)})
print(driver.execute_script("return navigator.userAgent;"))


# LOGIN
driver.get("https://info.bbdc.sg/members-login/")
time.sleep(int(random.choice(Rand_time))) # Pause

# inputting values into the user and pass entry boxes
user = "475Z31082001"
password = "314159"

user_input = driver.find_element_by_id("txtNRIC")
user_input.send_keys(user)
password_input = driver.find_element_by_id("txtPassword")
password_input.send_keys(password)
time.sleep(int(random.choice(Rand_time))) # Pause

# Press enter
password_input.send_keys(Keys.RETURN)


# PROCEED TO NEXT PAGE
proceed = driver.find_element_by_id("proceed-button")
proceed.click()


# HOMEPAGE
# Switching to left frame and clicking booking
driver.switch_to.default_content()
wait = WebDriverWait(driver, 300)
# Switching to the left frame
wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_name("leftFrame")))
booking = driver.find_element_by_link_text("Booking")
time.sleep(int(random.choice(Rand_time))) # Pause
booking.click()


# SELECT TPDS MOD
# Reseting the browser
driver.switch_to.default_content()
wait = WebDriverWait(driver, 300)
# Switching to the main frame
wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_name("mainFrame")))
select = driver.find_element_by_xpath("//html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[3]/td/input[2]")
select.click()
time.sleep(int(random.choice(Rand_time))) # Pause
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn"))).click()


# MONTH AND SESSION SELECTION
# Selection menu, waiting for content to load
driver.switch_to.default_content()
wait = WebDriverWait(driver, 300)
wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_name("mainFrame")))
wait.until(EC.visibility_of_element_located((By.ID, "checkMonth")))

# Select num of months
months = driver.find_elements_by_id("checkMonth")
number_of_months = 2
for i in range(number_of_months):
    months[i].click()
time.sleep(int(random.choice(Rand_time))) # Pause

# Select all sessions
session = driver.find_element_by_name("allSes")
session.click()
time.sleep(int(random.choice(Rand_time))) # Pause

# Select all days
days = driver.find_element_by_name("allDay")
days.click()
time.sleep(int(random.choice(Rand_time))) # Pause

while True:
    # Try the whole search to back/ search to found loop. If fail, break and restart the browser
    try:
        # Search
        time.sleep(int(random.choice(Rand_time))) # Pause
        driver.find_element_by_name("btnSearch").click()


        # SLOT SELECTION PAGE
        dates = []
        driver.switch_to.default_content()
        wait = WebDriverWait(driver, 300)
        wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_name("mainFrame")))

        body = driver.find_element_by_tag_name("body")
        msg = "There is no more slots available"

        if msg in body.text:
            backk = driver.find_element_by_name("btnBack")
            time.sleep(int(random.choice(Rand_time))) # Pause
            backk.click()
            counter += 1
            print(f"---No dates avaliable, going back!!! ({counter})---")

        else:

            # scrapes 2 earliest dates
            element1 = driver.find_element_by_xpath("//html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[9]/td/table/tbody/tr[3]/td[1]")
            element2 = driver.find_element_by_xpath("//html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[9]/td/table/tbody/tr[4]/td[1]")
            list1 = str(element1.text).split()
            list2 = str(element2.text).split()
            dates.append(str(list1[0]))
            dates.append(str(list2[0]))
            print(dates)

            # Check if dates match
            def checkdate(dates):
                # Dates to look out for
                dates_to_search = ["/02/", "/03/"]

                # Dates to avoid
                today = date.today()
                today_date = today.strftime("%d/%m/%Y")

                avoid = [today_date]
                
                for day in dates:
                    for search in dates_to_search:
                        if search in day and day not in avoid:
                            return True

            time.sleep(int(random.choice(Rand_time))) # Pause

            # If match, break inner loop
            if checkdate(dates):
                print("---Date match has been found, success!!!---")
                break

            # Go back to refresh search
            counter += 1
            print(f"---Dates did not match, going back again!!! ({counter})---")
            back = driver.find_element_by_xpath("//html/body/table/tbody/tr/td[2]/form/table[2]/tbody/tr[1]/td[1]/input[1]")
            back.click()
    # prints page and breaks the loop
    except:
        error = driver.find_element_by_tag_name("body")
        print(error.text)
        break

    # Reload page with a different useragent if more than 10 minutes
    time_limit = 600
    if time.time() - loop_time > time_limit:
        driver.close()
        break

# Select choice in the list of choices
try:
    choices = driver.find_elements_by_name("slot")

    # Try choice
    for choice in choices:
        try:
            choice.click()
            print("---Slot successfully chosen---")
            break
        except:
            pass

    # Submit order
    submit = driver.find_element_by_xpath("//html/body/table/tbody/tr/td[2]/form/table[2]/tbody/tr[1]/td[1]/input[2]")
    time.sleep(int(random.choice(Rand_time))) # Pause   
    submit.click()  
    

    # COMFIRMATION PAGE
    driver.switch_to.default_content()
    wait = WebDriverWait(driver, 300)
    wait.until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_name("mainFrame")))
    try:
        final = driver.find_element_by_xpath("//html/body/table/tbody/tr/td[2]/form/table/tbody/tr[14]/td[2]/input[2]")
        time.sleep(int(random.choice(Rand_time))) # Pause
        final.click()
        print("---Slot successfully booked---")
    except:
        pass
    finally:
        break
except:
    pass

print("---Restarting browser with new user agent---")

print(f"---Runtime: {round(time.time() - start_time)}s---")