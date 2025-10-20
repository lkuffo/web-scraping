"""
Objetivo: 
   - Extraer datos de un tag script
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 19 OCTUBRE 2025
"""
import requests
import json
from bs4 import BeautifulSoup 

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

url = "https://footdistrict.com/air-jordan-11-retro-rare-air-ih0296-400.html"

resp = requests.get(url, headers=headers)

soup = BeautifulSoup(resp.text, features="lxml")
print(soup)

# Las tallas cargan dinamicamente, e inicialmente se encuentran
# dentro de un JSON en el tag script
scripts = soup.find_all('script')
for script in scripts:
    contenido = script.contents
    if len(contenido) > 0:
        script = contenido[0]
        if "Talla" in script:
            texto_script = script
objeto = json.loads(texto_script) # Cargo el json a un diccionario
# Sabiendo la estructura del diccionario lo recorro para obtener la informacion que quiero
tallas = objeto['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']['jsonConfig']['attributes']['134']['options']
for talla in tallas:
  if "No disponible" not in talla["label"]: # filtro las tallas que no estan disponibles
    print (talla["label"]) # Imprimo por pantalla
