"""
OBJETIVO:  
    - Extraer los datos que se encuentran posterior a la resolucion de un CAPTCHA.
    - Aprender a resolver captchas de manera manual.
    - Aprender a descargar datos de iframes a traves de Selenium.
    - Aprender a evaluar si es que vale la pena extraer datos detras de un captcha.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 17 ABRIL 2020
"""
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36")

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

try:

  # Para interactuar con los elementos dentro de un iframe tengo que realizar
  # un cambio de contexto hacia el iframe
  driver.switch_to.frame(driver.find_element_by_xpath('//iframe'))
  # Luego yo ya puedo buscar elementos dentro del iframe e interactuar con estos
  captcha = driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-border"]')
  captcha.click()

  # El script se detiene para esperar que el usuario aplaste ENTER luego de resolver el catpcha
  input()

  # Una vez resuelto el captcha, devolvemos el driver al contexto de la pagina principal
  # Es decir, salimos del iframe
  driver.switch_to.default_content()

  # Damos click en el boton de submit
  submit_button = driver.find_element_by_xpath('//input[@id="recaptcha-demo-submit"]')
  submit_button.click()

except Exception as e:
  print (e)

# Me voy a encontrar aqui solamente si he resuelto el captcha
print ("Ya debo de estar en la pagina con la informacion...")

# Extraigo la informacion que estaba detras del captcha
contenido = driver.find_element_by_class_name('recaptcha-success')
print (contenido.text)