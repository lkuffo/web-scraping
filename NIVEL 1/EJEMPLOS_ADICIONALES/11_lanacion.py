import requests
from bs4 import BeautifulSoup 

# URL SEMILLA
url = 'https://www.lanacion.com.ar/opinion/seguro-desempleo-debate-impostergable-nid2444396'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url)

soup = BeautifulSoup(respuesta.text)

article = soup.find(id="nota")
parrafos = article.find_all('p')
for parrafo in parrafos:
  print (parrafo.text)