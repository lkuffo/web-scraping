# -*- coding: utf-8 -*-
"""
OBJETIVO: 
    - Extraer tweets de la pagina principal de twitter.
    - Aprender a llenar formularios desde Selenium.
    - Aprender a realizar extracciones que requieren autenticacion.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 17 ABRIL 2020
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

driver = webdriver.Chrome('./chromedriver.exe', options=opts)
driver.get('https://twitter.com/login')

user = "leonardokuffo"
password = open('password.txt').readline().strip()


# Me doy cuenta que la pagina carga el formulario dinamicamente luego de que la carga incial ha sido completada
# Por eso tengo que esperar que aparezca 
input_user = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//input[@name="session[username_or_email]"]'))
)
# Obtengo los inputs de usuario (linea 28) y password
input_pass = driver.find_element(By.XPATH, '//input[@name="session[password]"]')

# Escribo mi usuario input
input_user.send_keys(user)

# Escribo mi contrasena en el input
input_pass.send_keys(password)

# Obtengo el boton de login
login_button = driver.find_element(By.XPATH, '//main//div[@data-testid="LoginForm_Login_Button"]/div[@dir="auto"]')
# Le doy click
login_button.click()

# Espero a que aparezcan los tweets
tweets = WebDriverWait(driver, 10).until(
  EC.presence_of_all_elements_located((By.XPATH, '//section//article//div[@lang="en"]')) # Este xpath podria ser mejor
)

# Imprimo el texto de los tweets
for tweet in tweets:
  print(tweet.text)

# PARA INVESTIGAR:
# Porque no se obtienen todos los tweets que cargamos?
# Investiga que es Recycling Components en las interfaces webs
# https://medium.com/@moshe_31114/building-our-recycle-list-solution-in-react-17a21a9605a0