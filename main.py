import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# I was looking at some scripts for cookie clicker and got sort of dissappointed in the logic for choosing upgrades. Most of them was random or just hardcoded in values. 
# So, I want to make one that uses a smidge of reasonable logic. It will be valuing and choosing what to upgrade dependant on how many cookies it costs per increase in cookies per second.
# Doing the actual evaluation proved itself to be very time consuming in the context of how fast it can click. 
# It is slow because the cps value is in the tooltip which means the mouse has to hover over each building with actionchains in order to able to fetch it.
# Effort is put towards decreasing the number of evals put still putting that number to use.
# Its a balancing act of how often an eval should be done. If evals were as fast as a click then this would be a non-issue.

clicks_threshold = 100 # Higher is longer time between shopping
cookies_per_cps = 1000.0 # Less is better
clicks = 0
number_of_purchases_per_eval = 4
number_of_purchases_per_eval_counter = 0
classic = True

ser = Service("C:\Program Files (x86)\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(service=ser,options=options)

#driver.maximize_window()

# Using the in-game timer was needlessly complicated
#elapsed_Time_Text_List = driver.find_element(By.XPATH, '//*[@id="ascendTooltip"]/b').get_attribute('innerText').split()
#elapsed_Time = int(elapsed_Time_Text_List[elapsed_Time_Text_List.index('seconds')-1])

def evaluate_building(prod_numb):
    try:
        element = driver.find_element(By.XPATH, '//*[@id="product'+prod_numb+'"]')
        webdriver.ActionChains(driver).move_to_element(element).perform()
        if(driver.find_element(By.XPATH, '//*[@id="tooltip"]/div/small').get_attribute("outerText") == "[owned : 0"):
            element.click()
            return 0.0
        current_Cursor_increase_in_cps = float(driver.find_element(By.XPATH, '//*[@id="tooltip"]/div/div[7]/b[1]').get_attribute("outerText")) # gets the cookies per second
        current_Cursor_Price = float(driver.find_element(By.XPATH, '//*[@id="productPrice'+prod_numb+'"]').get_attribute("outerText").replace(",", "")) # gets the current price
        return (current_Cursor_Price / current_Cursor_increase_in_cps)
    except:
        pass
    return 0.0

def evaluate_building2(prod_numb):
    try:
        current_Cursor_Price = float(driver.find_element(By.XPATH, '//*[@id="productPrice'+prod_numb+'"]').get_attribute("outerText").replace(",", "")) # gets the current price
    except:
        return 0.0
    return current_Cursor_Price

if(classic): # Open and play classic cookie clicker
    which_product_to_click = ["Cursor",cookies_per_cps]
    driver.get("https://orteil.dashnet.org/experiments/cookie/")
    time.sleep(3)
    while(True):
        driver.find_element(By.XPATH, '//*[@id="cookie"]').click()
        clicks += 1
        if(clicks >= clicks_threshold):
            clicks = 0
            storeBuildings = driver.find_element(By.XPATH, '//*[@id="store"]').find_elements(By.TAG_NAME, 'DIV')
            for building in storeBuildings:
                textContentOfBuildingList = building.find_element(By.XPATH, '//*/b').get_attribute("textContent").split()
                #costBuilding = float(textContentOfBuildingList[-1])
                print("Building cost:",textContentOfBuildingList)
                # if(costBuilding < which_product_to_click[1]):
                #     which_product_to_click[1] = costBuilding
                #     which_product_to_click[0] = textContentOfBuildingList[0]
            #print("I am going to buy:",which_product_to_click[0])
            #driver.find_element(By.XPATH, '//*[@id="buy'+which_product_to_click[0]+'"]').click()
            



    driver.quit()
else: # Open and play new cookie clicker
    which_product_to_click = ["product0",cookies_per_cps]
    driver.get("https://orteil.dashnet.org/cookieclicker/")
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="statsButton"]').click()
    while(True):
        driver.find_element(By.XPATH, '//*[@id="bigCookie"]').click()
        clicks += 1

        if(clicks >= clicks_threshold):
            print("##### START OF A NEW CLICK RESET! ####")

            ##### Purchase building dependant on its cookies to cps ratio ######       
            if(number_of_purchases_per_eval_counter >= number_of_purchases_per_eval):
                number_of_purchases_per_eval_counter = 0
                which_product_to_click[1] = cookies_per_cps
                for x in range(0, 5):
                    eval_value = evaluate_building(str(x))
                    print("The eval value:",eval_value)
                    print("The value in list",which_product_to_click[1])
                    if((eval_value < which_product_to_click[1]) and (eval_value != 0.0)):
                        which_product_to_click[1] = eval_value
                        which_product_to_click[0] = "product"+str(x)
            
            try:
                driver.find_element(By.XPATH, '//*[@id="'+which_product_to_click[0]+'"]').click() # The surviving product upgrade will be clicked
            except:
                pass 
            
            ###### The store upgrades ######

            try:
                #driver.find_element(By.XPATH, '//*[@id="upgrades"]'))#.find_elements(By.CLASS_NAME, "crate upgrade enabled")
                element = driver.find_element(By.XPATH, '//*[@id="upgrade0"]')
                webdriver.ActionChains(driver).move_to_element(element).click().perform()
            except:
                pass
            number_of_purchases_per_eval_counter += 1
            clicks = 0
    driver.quit()