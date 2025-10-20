"""
OBJETIVO: 
    - Extraer archivos utilizando Web Scraping
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 20 OCTUBRE 2025
"""
import requests
from bs4 import BeautifulSoup

url_semilla = "https://file-examples.com/index.php/sample-documents-download/sample-xls-download/"

resp = requests.get(url_semilla)
soup = BeautifulSoup(resp.text, 'lxml')

urls = []

descargas = soup.find_all('a', class_="download-button")
for descarga in descargas:
    urls.append(descarga["href"])
print(urls)
i = 0
for url in urls: # Por cada url de los archivos que quiero descargar
    # Ver: https://www.udemy.com/instructor/communication/qa/17962324/detail?course=2861742
    url = url.replace("file-examples.com/wp-content/storage/", "file-examples.com/storage/fe519944ff66ba53b99c446/")
    
    r = requests.get(url, allow_redirects=True)
    nombre_archivo = './archivos/' + url.split('/')[-1]
    output = open(nombre_archivo, 'wb')
    output.write(r.content) # Escribir el archivo en mi PC
    output.close()
    i += 1

