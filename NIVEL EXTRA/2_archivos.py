"""
OBJETIVO: 
    - Extraer archivos utilizando Web Scraping
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 10 JULIO 2020
"""
import requests
from bs4 import BeautifulSoup

url_semilla = "https://file-examples.com/index.php/sample-documents-download/sample-xls-download/"

resp = requests.get(url_semilla)
soup = BeautifulSoup(resp.text)

urls = []

descargas = soup.find_all('a', class_="download-button")
for descarga in descargas:
    urls.append(descarga["href"])

i = 0
for url in urls: # Por cada url de los archivos que quiero descargar
    r = requests.get(url, allow_redirects=True)
    file_name = './archivos/excel-file-' + str(i) + '.xls'
    output = open(file_name, 'wb')
    output.write(r.content) # Escribir el archivo en mi PC
    output.close()
    i += 1

