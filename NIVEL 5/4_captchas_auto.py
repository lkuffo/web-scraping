"""
OBJETIVO:  
    - Extraer los datos que se encuentran posterior a la resolucion de un CAPTCHA.
    - Aprender a resolver captchas de manera automatica.
    - Aprender a utilizar el API de 2CAPTCHA. Un servicio resolvedor de captchas.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 09 ENERO 2023
"""
from selenium import webdriver
from time import sleep
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

driver = webdriver.Chrome('./chromedriver', chrome_options=opts)

url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

try:

  # Obtengo el identificador unico del catpcha
  captcha_key = driver.find_element(By.ID, 'recaptcha-demo').get_attribute('data-sitekey')
  
  # Armo el requerimiento a 2captcha
  url = "https://2captcha.com/in.php?"
  url += "key=" + "deb56d806b426e7372d84efb4f513246" # API KEY 2CAPTCHA
  url += "&method=userrecaptcha"
  url += "&googlekey=" + captcha_key
  url += "&pageurl=" + url
  url += "&json=0"

  print (url) # Visualizo URL

  # Hago un requerimiento GET con requests a la URL del API de 2captcha
  respuesta_requerimiento = requests.get(url)
  # Ellos encolan el captcha para ser resuelto y nos dan un ID para consultar el estado del catpcha
  captcha_service_key = respuesta_requerimiento.text

  print (captcha_service_key)
  # Parseo la respuesta para obtener el ID que nuestro captcha tiene en el sistema de 2CAPTCHA
  captcha_service_key = captcha_service_key.split('|')[-1]

  # Armo el requerimiento para consultar si el captcha ya se encuentra resuelto
  url_resp = "https://2captcha.com/res.php?"
  url_resp += "key=" + "2CAPTCHA_API_KEY_VER_DESCRIPCION_CLASE" # API KEY
  url_resp += "&action=get"
  url_resp += "&id=" + captcha_service_key # ID del captcha en el sistema de 2CAPTCHA obtenido previamente
  url_resp += "&json=0"

  print (url_resp)

  # Espero 20 segundos tal y como me lo indican sus instrucciones
  sleep(20)

  # Entro en un lazo para consultar el estado del captcha hasta que este resuelto
  while True:
    respuesta_solver =  requests.get(url_resp)
    respuesta_solver = respuesta_solver.text
    print (respuesta_solver)
    # Si el captcha no esta listo, espero 5 segundos, itero nuevamente en el lazo y vuelvo a preguntar
    if respuesta_solver == "CAPCHA_NOT_READY":
      sleep(5)
    # Caso contrario el captcha esta resuelto y puedo romper el lazo
    else: 
      break

  # Obtengo la solucion del captcha que me devolvio el API de 2CAPTCHA
  respuesta_solver = respuesta_solver.split('|')[-1]
  print ()
  # Utilizo el script que tienen en su documentacion para insertar la solucion dentro de la pagina web
  insertar_solucion = 'document.getElementById("g-recaptcha-response").innerHTML="' + respuesta_solver + '";'
  print (insertar_solucion)

  # Ejecuto el script con selenium
  driver.execute_script(insertar_solucion)

  # Doy click en el boton de submit y deberia avanzar
  submit_button = driver.find_element('xpath', '//input[@id="recaptcha-demo-submit"]')
  submit_button.click()
except Exception as e:
  print (e) 

# Logica una vez resuelto el captcha o si no existio nunca el captcha
print ("Ya debo de estar en la pagina donde esta la informacion...")

# Extraigo la informacion detras del captcha
contenido = driver.find_element(By.CLASS_NAME, 'recaptcha-success')
print (contenido.text)