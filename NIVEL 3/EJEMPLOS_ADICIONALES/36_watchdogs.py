import re, random
from time import sleep
# SELENIUM:
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
 
# SELENIUM (Initializing the main page):
 
opts = Options()
opts.add_argument('--disable-blink-features=AutomationControlled')
# Creating our driver:
driver = webdriver.Chrome("./chromedriver", options=opts)
driver.get("https://www.watchdogsecurity.online/")
 
 
# RETREIVING THE DATA FROM THE FILES. THIS DATA IS GOING TO BE USED TO FILL IN THE FORM:
Name = 'Juanito Perez'
Email = 'juanito@gmail.com'
message = 'HOLA MUNDO'
urls = ["www.google.com", "www.youtube.com"]
 
# THE ALGORITHM TO FILL THE FORM STARTS:
for url in urls:
    # FORM ELEMENTS:
    name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='input_comp-kexbfbko']")),
    )
 
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='input_comp-kexbfbky']")),
    )
 
    infringe_url_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='input_comp-kexbfbl1']")),
    )
 
    message_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@id='textarea_comp-kexbfbl41']")),
    )
 
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='comp-kexbfblb']/button"))
    )
 
    sleep(random.uniform(1.0, 2.0))
    name_field.send_keys(Name)
    email_field.send_keys(Email)
    infringe_url_field.send_keys(url)
    message_field.send_keys(message)
 
    sleep(random.uniform(3.0,3.5))
    driver.refresh()
 
    # sleep(random.uniform(1.5,2.0))
    # button.click()
    # sleep(random.uniform(2.5,3.0))
 
driver.close()