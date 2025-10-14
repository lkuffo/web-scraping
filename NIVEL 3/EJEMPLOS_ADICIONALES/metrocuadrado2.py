from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date
from datetime import datetime
 
Ftoday = date.today().strftime('%d%m%Y')
Fecha = date.today().strftime('%d-%m-%Y')
 
# Definimos el User Agent en Selenium utilizando la clase Options
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
#opts.add_argument('-headless')
driver = webdriver.Chrome('./chromedriver', chrome_options=opts) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
 
#URL SEMILLA
 
start_urls = [# "https://www.metrocuadrado.com/oficina/venta/nuevo/medellin/",
    "https://www.metrocuadrado.com/oficina/venta/usado/medellin/",
    "https://www.metrocuadrado.com/oficina/venta/nuevo/bogota/",
    "https://www.metrocuadrado.com/oficina/venta/usado/bogota/"]
 
i=0
for url in start_urls:
    driver.get(url)
 
    if "medellin" in url:
        Ciudad="Medellín"
    else:
        Ciudad="Bogotá"
        
    if "usado" in url:
        Estado="Usado"
    else:
        Estado="Nuevo"
        
    if "venta" in url:
        Tipo="Venta"
    else:
        Tipo="Renta"
    
    f = open("./"+Tipo+" "+Estado+" "+Ciudad+" "+Ftoday+".csv", "a")
    f.write("Código_inmueble" + ";" + "Descripción" + ";" +"Descripción2" +";" + "Ciudad"+ ";" + "Precio" + ";" + "Barrio_común" +";" + "Barrio_catastral" +";" + "Antigüedad" +";" + "Área_construida" +";" + "Área_privada" +";" + "Precio_M2" +";" + "URL" +";" +"Estado"+";" +"Tipo"+";" +"Fecha" +"\n")
    f.close()
 
    #PAGINACION_MAX = 3
    #PAGINACION_ACTUAL = 1
 
    # Mientras la pagina en la que me encuentre, sea menor que la maxima pagina que voy a sacar... sigo ejecutando...
    #while PAGINACION_MAX >= PAGINACION_ACTUAL:
    while True:     
      # Cerramos el mensajito de disclaimer para que no interfiera con el click a la flecha de siguiente
      sleep(1)
      try:
        driver.find_element(By.XPATH, '//a[contains(@class, "btn-disclaimer")]').click()
      except:
        print ("Disclaimer no encontrado")
        
      try:
        elem = driver.find_element(By.XPATH, '//form/div[5]/div/div[1]/div[@class="m2-select-container"]').click()
        myDesiredValue = driver.find_element(By.XPATH, '//form/div[5]/div/div[1]/div[@class="m2-select-container"]//div[contains(text(), "500")]').click()
      except Exception as e: 
        print("error", e)

        
      sleep(5)  

      links_productos = driver.find_elements(By.XPATH, '//div[@class="card-header"]//a')
      links_de_la_pagina = []
      print ('links_productos', links_productos)
    
      for a_link in links_productos:    
        links_de_la_pagina.append(a_link.get_attribute("href"))
      print ('links_de_la_pagina', links_de_la_pagina)
 
      for link in links_de_la_pagina:
        
        try:
          # Voy a cada uno de los links de los detalles de los productos
 
          sleep(3)
 
          # ABRO UN NUEVO TAB CON LA URL DEL DETALLE DEL PRODUCTO
          # PARA NO PERDER LA PAGINACION
          driver.execute_script("window.open('{}');".format(link))
          driver.switch_to.window(driver.window_handles[1])
          URL = link
          
          if Estado=="Usado": 
            Descripción=driver.find_element(By.XPATH,'//div[3]//h1').text              
            Descripción2=driver.find_element(By.XPATH,'//div[2]/div[2]/div[3]/div[1]/div/p').text
            Precio=driver.find_element(By.XPATH,'//div[8]//h3[contains(text(),"Precio")]/following-sibling::p').text
              #Baños=driver.find_element(By.XPATH,'//li[2]/div/h2').text
              #Estrato=driver.find_element(By.XPATH,'//li[3]/div/h2').text
            Código_inmueble=driver.find_element(By.XPATH,'//div[8]//h3[contains(text(),"Código inmueble")]/following-sibling::p').text
            Barrio_común=driver.find_element(By.XPATH,'//div[8]//h3[contains(text(),"Barrio común")]/following-sibling::p').text
            Barrio_catastral=driver.find_element(By.XPATH,'//div[8]//h3[contains(text(),"Barrio catastral")]/following-sibling::p').text   
            Antigüedad=driver.find_element(By.XPATH,'//div[8]//h3[contains(text(),"Antigüedad")]/following-sibling::p').text
            Área_construida=driver.find_element(By.XPATH,'//div[8]//h3[contains(text(),"Área construida")]/following-sibling::p').text
            Área_privada=driver.find_element(By.XPATH,'//div[8]//h3[contains(text(),"Área privada")]/following-sibling::p').text
          else:
            Descripción=driver.find_element(By.XPATH,'//div[3]/div[1]//h1').text              
            Descripción2=driver.find_element(By.XPATH,'//div[2]/div[2]/div[3]/div[1]/div/p').text
            Precio=driver.find_element(By.XPATH,'//div[6]//h3[contains(text(),"Precio")]/following-sibling::p').text
          #Baños=driver.find_element(By.XPATH,'//li[2]/div/h2').text
          #Estrato=driver.find_element(By.XPATH,'//li[3]/div/h2').text
            Código_inmueble=driver.find_element(By.XPATH,'//div[6]//h3[contains(text(),"Código inmueble")]/following-sibling::p').text
            Barrio_común=driver.find_element(By.XPATH,'//div[6]//h3[contains(text(),"Barrio común")]/following-sibling::p').text
            Barrio_catastral=driver.find_element(By.XPATH,'//div[6]//h3[contains(text(),"Barrio catastral")]/following-sibling::p').text   
            Antigüedad=driver.find_element(By.XPATH,'//div[6]//h3[contains(text(),"Estado")]/following-sibling::p').text
            Área_construida=driver.find_element(By.XPATH,'//div[6]//h3[contains(text(),"Área construida")]/following-sibling::p').text
            Área_privada=driver.find_element(By.XPATH,'//div[6]//h3[contains(text(),"Área privada")]/following-sibling::p').text
            
        
          Código_inmueble =Código_inmueble.replace('\n', '').replace('\r', '').strip()
          Descripción = Descripción.replace('\n', '').replace('\r', '').strip()
          Descripción2 = Descripción2.replace('\n', '').replace('\r', '').strip()
          Ciudad = Ciudad.replace('\n', '').replace('\r', '').strip()
          Precio = Precio.replace('$', '').replace('.', '').strip()
          Barrio_común=Barrio_común.replace('\n', '').replace('\r', '').strip()
          Barrio_catastral=Barrio_catastral.replace('\n', '').replace('\r', '').strip()
          Antigüedad=Antigüedad.replace('\n', '').replace('\r', '').strip()
          Área_construida=Área_construida.replace('m²', '').replace('\n', '').replace('\r', '').strip()
          Área_privada=Área_privada.replace('m²', '').replace('\n', '').replace('\r', '').strip()
          
          try:
            Precio_M2= str(float(Precio)/float(Área_construida))
          except Exception as e:
            Precio_M2=str(0)
          
        
        # Guardado de datos en un archivo
 
          f = open("./"+Tipo+" "+Estado+" "+Ciudad+" "+Ftoday+".csv", "a")
          f.write(Código_inmueble + ";" + Descripción + ";" + Descripción2 + ";" + Ciudad + ";" + Precio + ";" + Barrio_común +";" + Barrio_catastral +";" + Antigüedad +";" + Área_construida +";" + Área_privada +";" + Precio_M2 +";" + URL +";" +Estado+";" +Tipo+";" +Fecha +"\n")
          f.close()
 
          #print(Código_inmueble)
          #print(Descripción)
          #print(Descripción2)
          #print(Ciudad)
          #print(Precio)
          #print(Barrio_común)
          #print(Barrio_catastral)
          #print(Antigüedad )
          #print(Área_construida)
          #print(Área_privada )
          #print(Precio_M2)
 
          # Aplasto el boton de retroceso
          driver.close()
          driver.switch_to.window(driver.window_handles[0])
          i=i+1
          print(i)  
        
        except Exception as e:
          print ('Error dummer', e)
          # Si sucede algun error dentro del detalle, no me complico. Regreso a la lista y sigo con otro producto.
          driver.close()
          driver.switch_to.window(driver.window_handles[0])
 
      # Logica de deteccion de fin de paginacion
      try:
        # Intento obtener el boton de SIGUIENTE y le intento dar click
        puedo_seguir_horizontal = driver.find_element(By.XPATH, '//li[@class="item-icon-next page-item"]/a')
        puedo_seguir_horizontal.click()
      except Exception as e: 
        # Si no puedo es porque ya estoy al final de la paginacion. BREAK
        print("error", e)
        break
        
      #PAGINACION_ACTUAL += 1