import time

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By


ser = Service("C:\Program Files (x86)\chromedriver.exe")

options = webdriver.ChromeOptions()

options.add_argument("--incognito")

driver = webdriver.Chrome(service=ser,options=options)

driver.get("https://orteil.dashnet.org/cookieclicker/")

driver.maximize_window()


# I was looking at some scripts for cookie clicker and got very dissappointed in the most available programming logic. That is more or less the genesis of this stupid script.


time.sleep(3)

# Using the in-game timer was needlessly complicated
#elapsed_Time_Text_List = driver.find_element(By.XPATH, '//*[@id="ascendTooltip"]/b').get_attribute('innerText').split()
#elapsed_Time = int(elapsed_Time_Text_List[elapsed_Time_Text_List.index('seconds')-1])

clicks = 0

while(True):
    driver.find_element(By.XPATH, '//*[@id="bigCookie"]').click()
    clicks += 1
    if(clicks >= 100):
        driver.find_element(By.XPATH, '//*[@id="product0"]').click()
        try:
            current_Cursor_increase_in_cps = float(driver.find_element(By.XPATH, '//*[@id="tooltip"]/div/div[7]/b[1]').get_attribute("outerText")) # gets the cookies per second
            print(current_Cursor_increase_in_cps)
        except:
            pass
        current_Cursor_Price = int(driver.find_element(By.XPATH, '//*[@id="productPrice0"]').get_attribute("outerText")) # gets the current price
        #print(current_Cursor_increase_in_cps)
        clicks = 0
    

driver.quit()