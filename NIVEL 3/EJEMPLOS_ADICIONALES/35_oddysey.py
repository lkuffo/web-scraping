from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
 
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
)
 
driver = webdriver.Chrome("./chromedriver", options=opts)
 
driver.get('https://listado.mercadolibre.com.pe/videojuegos/super-mario-odyssey')
 
# Debemos darle click al boton de disclaimer para que no interrumpa nuestras acciones
try: # Encerramos todo en un try catch para que si no aparece el discilamer, no se caiga el codigo
  disclaimer = driver.find_element(By.XPATH, '//button[@id="cookieDisclaimerButton"]')
  disclaimer.click() # lo obtenemos y le damos click
except Exception as e:
  print (e) 
  None

try:
    boton_siguiente = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
    boton_siguiente.click()
except:
    print("Hubo un error")