""" 
Consulta y Descarga de documentos. Leyendo los IDS del documento de un archivo.
(Todos los IDs dentro del archivo ids.txt son INVALIDOS por seguridad)
"""
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

driver = webdriver.Chrome('./chromedriver') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
 
# Voy a la pagina que requiero
driver.get('https://www.procuraduria.gov.co/CertWEB/Certificado.aspx')
# Selecciono el tipo de documento a buscar
boton = driver.find_element_by_xpath('.//select[@class="ComboBox"]/option[2]')
boton.click()
 
#extraigo la pregunta
pregunta = driver.find_element_by_xpath('.//span[@id="lblPregunta"]').text
 
while pregunta != "¿ Cuanto es 2 X 3 ?":
    boton = driver.find_element_by_xpath('.//input[@type="image"]')
    boton.click()
    sleep(random.uniform(0.2, 0.5))
    pregunta = driver.find_element_by_xpath('.//span[@id="lblPregunta"]').text
 
respuesta= "6"

input_file = open('ids.txt')
for documento in input_file: # Itero cada linea de mi archivo (es decir, cada documento)
  documento = documento.strip() # elimino saltos de linea

  input_id = WebDriverWait(driver, 0.5).until(
    EC.presence_of_element_located((By.XPATH, './/input[@name="txtNumID"]'))
  )
  input_pregunta = driver.find_element(By.XPATH, './/input[@name="txtRespuestaPregunta"]')
  
  # Le hago clear a los inputs para escribir siempre desde cero
  input_id.clear()
  input_pregunta.clear()

  input_id.send_keys(documento)
  
  # Escribo mi contrasena en el input
  input_pregunta.send_keys(respuesta)
  
  # Busco el boton consultar
  login_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
  # Le doy click
  login_button.click()
  sleep(random.uniform(2, 2.5))
  
  validacion = driver.find_element_by_xpath('.//div[@id="ValidationSummary1"]').text
  if "NO SE ENCUENTRA" in validacion:
    continue # este continue, va a hacer qeu automaticamente nos movamos en la siguiente itearcion del lazo, es decir, la siguiente linea del archivo
  
  tercero = driver.find_element_by_xpath('.//div[@class="datosConsultado"]')
  
  primer_nombre = driver.find_element_by_xpath('.//div[@class="datosConsultado"]//span[1]').text
  segundo_nombre = driver.find_element_by_xpath('.//div[@class="datosConsultado"]//span[2]').text
  primer_apellido = driver.find_element_by_xpath('.//div[@class="datosConsultado"]//span[3]').text
  segundo_apellido = driver.find_element_by_xpath('.//div[@class="datosConsultado"]//span[4]').text
  
  
  f = open("./terceros.csv", "a")
  f.write(primer_nombre + "," + segundo_nombre + "," + primer_apellido + "," + segundo_apellido +"\n")
  f.close()
  
  print (primer_nombre)
  print (segundo_nombre)
  print (primer_apellido)
  print (segundo_apellido)

  


input_file.close()

