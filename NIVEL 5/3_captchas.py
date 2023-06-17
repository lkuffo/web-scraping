"""
OBJETIVO:  
    - Extraer los datos que se encuentran posterior a la resolucion de un CAPTCHA.
    - Aprender a resolver captchas de manera manual.
    - Aprender a descargar datos de iframes a traves de Selenium.
    - Aprender a evaluar si es que vale la pena extraer datos detras de un captcha.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 09 ENERO 2023
"""
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)

url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

try:

  # Para interactuar con los elementos dentro de un iframe tengo que realizar
  # un cambio de contexto hacia el iframe
  driver.switch_to.frame(driver.find_element('xpath', '//iframe'))
  # Luego yo ya puedo buscar elementos dentro del iframe e interactuar con estos
  captcha = driver.find_element('xpath', '//div[@class="recaptcha-checkbox-border"]')
  captcha.click()

  # El script se detiene para esperar que el usuario aplaste ENTER luego de resolver el catpcha
  input()

  # Una vez resuelto el captcha, devolvemos el driver al contexto de la pagina principal
  # Es decir, salimos del iframe
  driver.switch_to.default_content()

  # Damos click en el boton de submit
  submit_button = driver.find_element('xpath', '//input[@id="recaptcha-demo-submit"]')
  submit_button.click()

except Exception as e:
  print (e)

# Me voy a encontrar aqui solamente si he resuelto el captcha
print ("Ya debo de estar en la pagina con la informacion...")

# Extraigo la informacion que estaba detras del captcha
contenido = driver.find_element(By.CLASS_NAME, 'recaptcha-success')
print (contenido.text)