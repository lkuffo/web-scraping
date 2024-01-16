"""
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 2 DICIEMBRE 2020
"""
import requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

# URL SEMILLA
url = 'https://www.lanacion.com.ar/politica/victorias-derrotas-impuesto-nid2512832'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)

# PARSEO DEL ARBOL CON BEAUTIFUL SOUP
soup = BeautifulSoup(respuesta.text)
nota = soup.find(id="cuerpo") # ENCONTRAR UN ELEMENTO POR ID
parrafos = nota.find_all('p') # ENCONTRAR VARIOS ELEMENTOS POR TAG Y POR CLASE
for parrafo in parrafos: # ITERAR ELEMENTO POR ELEMENTO
  print (parrafo.text)


