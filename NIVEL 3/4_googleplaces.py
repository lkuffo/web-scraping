# -*- coding: utf-8 -*-
"""
OBJETIVO: 
    - Extraer resenas escritas por usuarios en Google Places.
    - Aprender a cargar informacion haciendo scrolling.
    - Aprender a manejar varios tabs abiertos al mismo tiempo en Selenium.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 17 ABRIL 2020
"""
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# User agent
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

# Funcion para obtener el Script de Scrolling dependiendo de cuantos scrollings ya he hecho
# Es un approach mas inteligente que el utilizado en el video. En donde, mientras mas escrolls llevo dando, mas pixeles voy bajando.
# Simplemente remplazo el 20000 en la cadena del script, por un numero que dependa de la iteracion en que me encuentro actualmente
def getScrollingScript(iteration): 
    # Script de scrolling es un script de javascript. Le hago scroll a un contenedor que contenta ciertas clases
    # Estas clases dependen de mi extraccion. Existen otras maneras de hacer scrolling que veremos en el NIVEL EXTRA.
    scrollingScript = """ 
      document.getElementsByClassName('section-layout section-scrollbox scrollable-y scrollable-show')[0].scroll(0, 20000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)
driver.get('https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423706!4d-3.6850768!9m1!1b1')

# A veces google places necesita una espera adicional para encontrarse verdaderamente cargado
sleep(random.uniform(4.0, 5.0))

# Logica de Scrolling
SCROLLS = 0
while (SCROLLS != 3): # Decido que voy a hacer 3 scrollings
  driver.execute_script(getScrollingScript(SCROLLS)) # Ejecuto el script para hacer scrolling del contenedor
  sleep(random.uniform(4, 5)) # Entre cada scrolling espero un tiempo
  SCROLLS += 1


# Una vez que ha terminado el scrollings...
# Obtengo la Lista de reviews del restaurante
restaurantsReviews = driver.find_elements(By.XPATH, '//div[contains(@class, "section-review ripple-container")]')

# Por cada review...
for review in restaurantsReviews:

  # Obtengo el contenedor del nombre de usuario
  userLink = review.find_element(By.XPATH, './/div[@class="section-review-title"]')

  try:

    userLink.click() # Damos click en el nombre de display del usuario para abrir su perfil. Esto se abre en un nuevo tab.

    # Movemos el contexto del driver al tab en la segunda posicion. Si no hacemos esto, no podremos acceder a los elementos del nuevo tab.
    driver.switch_to.window(driver.window_handles[1])

    # Damos click en el tab de opiniones del usuario, no sin antes esperar que este disponible
    opiniones_tab = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//button[@class="section-tab-bar-tab ripple-container section-tab-bar-tab-unselected"]'))
    )
    opiniones_tab.click()

    # Logica de Scrolling de las opiniones del usuario
    userReviews = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"section-review ripple-container")]'))
    )
    USER_SCROLLS = 0
    # Similar a la logica utilizada para hacer scrolling de las opiniones de un restaurante
    while (USER_SCROLLS != 3):
      driver.execute_script(getScrollingScript(USER_SCROLLS))
      sleep(random.uniform(4, 5))
      USER_SCROLLS += 1
    
    # Obtenemos todos los reviews visibles del usuario
    userReviews = driver.find_elements(By.XPATH,'//div[contains(@class,"section-review ripple-container")]')

    # Por cada review que ha hecho el usuario...
    for userReview in userReviews:
      # Obtener la informacion de cada review

      reviewRating = userReview.find_element(By.XPATH, './/span[@class="section-review-stars"]').get_attribute('aria-label')
      userParsedRating = float(''.join(filter(str.isdigit or str.isspace, reviewRating))) # Codigo para solamente quedarme con los digitos de una cadena. En la clase nos quedamos con toda la cadena.
      reviewText = userReview.find_element(By.XPATH, './/span[@class="section-review-text"]').text

      print (userParsedRating)
      print (reviewText)

    # Cerramos el tab que se nos abrio
    driver.close()
    # Movemos el contexto del driver al unico tab abierto, es decir el primero
    driver.switch_to.window(driver.window_handles[0])

  # Si ocurre algun error, no me complico, cierro el tab abierto, y reinicio el contexto al tab original
  except Exception as e:
      print(e)
      driver.close() 
      driver.switch_to.window(driver.window_handles[0])
