"""
OBJETIVO: 
    - Aprender a utilizar la librería Cloudscraper para páginas con protección de Cloudflare
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 JUNIO 2023
"""

import cloudscraper
import requests
from bs4 import BeautifulSoup 

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


url = 'https://www.zonaprop.com.ar/cocheras-alquiler-capital-federal.html'

# No funciona
# session = requests.Session()
# resp = session.get(url, headers=headers)
# print(resp.text)

scraper = cloudscraper.create_scraper()
response = scraper.get(url)
print(response)

soup = BeautifulSoup(response.text, features="lxml")

contenedor_de_anuncios = soup.find_all('div', {"data-qa": "posting PROPERTY"})
for div_anuncio in contenedor_de_anuncios:
    titulo = div_anuncio.find('h2').text
    print(titulo)