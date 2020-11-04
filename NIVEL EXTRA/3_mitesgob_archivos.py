import requests
from time import sleep
from lxml import html
 
anios_trabajo = [2014, 2015, 2016, 2017, 2018, 2019] # Lista de anios que quiero descargar
for anio in anios_trabajo:
  url = "http://www.mites.gob.es/es/estadisticas/monograficas_anuales/EAT/" + str(anio) + "/index.htm" # Me doy cuenta del patron de la URL
  resp = requests.get(url)
  parser = html.fromstring(resp.text)
 
  links = parser.xpath('//ul[@class="lista_horizontal"]/li/a/@href') # Obtengo todos los links de descarga con un XPATH
  for link in links:
    nombre_archivo = link.split('/')[-1] # Si el link es href="http://www.mites.gob.es/estadisticas/eat/eat17/TABLAS ESTADISTICAS/ATR_2017_Resumen.xls", la ultima parte del link es el nombre
    print (nombre_archivo)
    # No descargo todos los archivos, solamente si contiene la extension "xls"
    if 'xls' in nombre_archivo: # Aqui podriamos agregarle lo siguiente para solo descargar la seccion D: and "_D" in nombre_archivo
      # Descargo el archivo
      r = requests.get(link, allow_redirects=True)
      output = open(nombre_archivo, 'wb')
      output.write(r.content) # Escribir el archivo en mi PC
      output.close()
      sleep(1) # esperamos un poco para no saturar al servidor