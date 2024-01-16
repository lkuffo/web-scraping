"""
OBJETIVO: 
    - Actualización de Twitter 2023
CREADO POR: TOMAS ALLAMI (https://github.com/Tallami) y  LEONARDO KUFFO
ULTIMA VEZ EDITADO: 15 ENERO 2024
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)
driver.get('https://twitter.com/login')

user = "leonardokuffo"
password = open('password.txt').readline().strip()


# Me doy cuenta que la pagina carga el formulario dinamicamente luego de que la carga incial ha sido completada
# Por eso tengo que esperar que aparezca 
input_user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class = 'r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7']")))
input_user.send_keys(user)

# Obtengo el boton next y lo presiono para poder poner la pass
next_button = driver.find_element(By.XPATH, '(//div[@class="css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-usiww2 r-13qz1uu r-2yi16 r-1qi8awa r-ymttw5 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l"])[1]')
next_button.click()

# Obtengo los inputs de usuario (linea 28) y password
input_pass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')))
input_pass.send_keys(password)

# Obtengo el boton de login
login_button = driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]')
# Le doy click
login_button.click()

# Espero a que aparezcan los tweets
tweets = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# Imprimo el texto de los tweets
for tweet in tweets:
  print(tweet.text)