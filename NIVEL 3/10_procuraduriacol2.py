import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
  
driver = webdriver.Chrome('./chromedriver') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
# Voy a la pagina que requiero
driver.get('https://devolucion.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces')
 
input_file = open('ids.txt')
for documento in input_file: # Itero cada linea de mi archivo (es decir, cada documento)
  documento = documento.strip() # elimino saltos de linea
  print (len(documento))
  
  input_id = driver.find_element(By.XPATH, './/input[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit"]')
  # Le hago clear a los inputs para escribir siempre desde cero
  input_id.clear()
  input_id.send_keys(documento)

  # Busco el boton consultar
  login_button = driver.find_element(By.XPATH, './/input[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar"]')
  # Le doy click
  login_button.click()
  sleep(random.uniform(2, 2.5))
 
  try:
    boton_cerrar = driver.find_element(By.XPATH, '//div[@id="divMensaje"]//img[@onclick="cerrarLayer();"]')
    continue # si le pude dar click, es porque no se encontro el ID. Entonces, continuo con el siguiente ID en la iteracion
  except: # Si sucede un error, es porque no se ha encontrado el boton, por lo tanto puedo escribir mi logica que obtiene la informacion
   # logica para obtener el texto del resultado
   
   if len (documento) == 9: 
      razonsocial = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:razonSocial"]').text
      digitover = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv"]').text
      estado = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado"]').text
      f = open("./dian.csv", "a")
      f.write(documento + "," + razonsocial + "," + digitover + "," + estado + "\n")
      f.close()
      print (razonsocial)
      print (digitover)
      print (estado)
 
   elif len (documento) != 9:
 
      primer_nombre = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerNombre"]').text
      segundo_nombre = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:otrosNombres"]').text
      primer_apellido = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerApellido"]').text
      segundo_apellido = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:segundoApellido"]').text
      digitover = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv"]').text
      estado = driver.find_element_by_xpath('.//span[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado"]').text
      f = open("./dian.csv", "a")
      f.write(documento + "," + primer_nombre + "," + segundo_nombre + "," + primer_apellido + "," + segundo_apellido +","+ estado +","+ digitover +"\n")
      f.close()
      print (primer_nombre)
      print (segundo_nombre)
      print (primer_apellido)
      print (segundo_apellido)
      print (documento)
 
input_file.close()
   