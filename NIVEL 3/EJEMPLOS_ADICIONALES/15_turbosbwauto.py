import time
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver  ## pip install selenium # driver capturador de info en la web
from selenium.webdriver.chrome.options import Options  ## para enmascarar al robot
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
 
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36")
 
# instalando del driver de selenium que va a controlar nuestro navegador
# a partir de este objeto voy a crear web scraping e interacciones
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
 
# voy a la pagina que requiero
driver.get('http://www.turbos.bwauto.com/es/aftermarket/productSearch.aspx')

primermenu = driver.find_element_by_xpath("//select[@name='ctl00$MainContent$ddlMF']")
primermenu.click() # abro el menu

opcion1 = primermenu.find_element_by_xpath("//select[@name='ctl00$MainContent$ddlMF']/option[text()='Alpina']")
opcion1.click() # selecciono la opcion

sleep(5)

# Segui...