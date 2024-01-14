"""
OBJETIVO: 
  - Extraer las preguntas de la pagina principal de Stackoverflow
  - Aprender a utilizar Beautiful Soup para parsear el arbol HTML
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 09 ENERO 2024
"""
import requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

# URL SEMILLA
url = 'https://stackoverflow.com/questions'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)

# PARSEO DEL ARBOL CON BEAUTIFUL SOUP
soup = BeautifulSoup(respuesta.text)
contenedor_de_preguntas = soup.find(id="questions") # ENCONTRAR UN ELEMENTO POR ID
lista_de_preguntas = contenedor_de_preguntas.find_all('div', class_="s-post-summary") # ENCONTRAR VARIOS ELEMENTOS POR TAG Y POR CLASE
for pregunta in lista_de_preguntas: # ITERAR ELEMENTO POR ELEMENTO

  # METODO #1: METODO TRADICIONAL
  texto_pregunta = pregunta.find('h3').text # DENTRO DE CADA ELEMENTO ITERADO ENCONTRAR UN TAG
  descripcion_pregunta = pregunta.find(class_='s-post-summary--content-excerpt').text # ENCONTRAR POR CLASE
  descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\r', '') # LIMPIEZA DE TEXTO
  print (texto_pregunta)
  print (descripcion_pregunta)
  print ()


  # METODO #2: APROVECHANDO EL PODER COMPLETO DE BEAUTIFUL SOUP
  contenedor_pregunta = pregunta.find('h3')
  texto_pregunta = contenedor_pregunta.text
  descripcion_pregunta = contenedor_pregunta.find_next_sibling('div') # TRAVERSANDO EL ARBOL DE UNA MENERA DIFERENTE
  texto_descripcion_pregunta = descripcion_pregunta.text

  texto_descripcion_pregunta = texto_descripcion_pregunta.replace('\n', '').replace('\t', '')
  # print (texto_pregunta)
  # print (texto_descripcion_pregunta)
  # print ()



