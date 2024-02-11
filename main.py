#############################################
############## CHANGABLE PART ###############
#############################################
user_email = "email@itu.edu.tr"         
user_password = "password" 
                                           
wanted_crn = [21342, 21343, 20378] # max 12 crn 
unwanted_crn = [] # have to selected already, // for now
                                           
# year month day hour minute second        
time = [2024, 2, 7, 10, 00, 00]            
                                           
submit_limit = 600 # be careful not to block 
period = 0.05 # second    
#############################################




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import datetime

chrome_driver_path = './chromedriver-mac-arm64/chromedriver'
service = Service(chrome_driver_path)
service.start()
driver = webdriver.Chrome(service=service)
driver.get("https://kepler-beta.itu.edu.tr/ogrenci/DersKayitIslemleri/DersKayit")

email = driver.find_element(By.ID, "ContentPlaceHolder1_tbUserName")
email.send_keys(user_email)
pwd = driver.find_element(By.ID, "ContentPlaceHolder1_tbPassword")
pwd.send_keys(user_password)
enter_sis = driver.find_element(By.ID, "ContentPlaceHolder1_btnLogin")
enter_sis.click()


access1 = driver.find_element(By.CLASS_NAME, "icon-note")
access1.click()

desired_time = datetime.datetime(time[0], time[1], time[2], time[3], time[4], time[5]) - datetime.timedelta(seconds=3)
while (datetime.datetime.now() < desired_time):
    remaining_time = desired_time - datetime.datetime.now()
    print(f"Remaining time: {remaining_time}")
    sleep(1)

print("Ready!!")
access2 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/ogrenci/DersKayitIslemleri/DersKayit']")))
ActionChains(driver).move_to_element(access2).perform()
access2.click()

crn = wanted_crn + unwanted_crn
crn_rows = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='row mb-5']")))
input_rows = crn_rows.find_elements(By.XPATH, ".//input[@type='number']")

submit_count = 0
while((submit_count < submit_limit) & (datetime.datetime.now() > desired_time)):
    submit_count += 1

    i = 0
    for input_element in input_rows:
        if(i == len(crn)):
            break
        input_element.send_keys(str(crn[i]))
        i += 1

    for unw_element in unwanted_crn:
        unw_crn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{unw_element}')]")))
        unw_crn.click()
    
    conf1 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-step='3' and @data-title='İşlem Yap']")))
    conf1.click()
    conf2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn ml-2 btn btn-success']")))
    conf2.click()
    print(submit_count)
    sleep(period)


sleep(20)
driver.quit()