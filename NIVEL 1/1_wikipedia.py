"""
OBJETIVOS: 
    - Extraer los idiomas de la pagina principal de WIKIPEDIA
    - Aprender a utilizar requests para hacer requerimientos
    - Aprender a utilizar lxml para parsear el arbol HTML
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 14 ENERO 2024
"""
import requests # pip install requests
from lxml import html # pip install lxml

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# URL SEMILLA
url = 'https://www.wikipedia.org/'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)
respuesta.encoding = 'utf-8' # Codificar correctamente caracteres extranos

# PARSEO DEL ARBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
parser = html.fromstring(respuesta.content) # Uso .content para poder codificar los caracteres raros

# EXTRACCION DE IDIOMA INGLES
ingles = parser.get_element_by_id("js-link-box-en")
print (ingles.text_content())

# EXTRACCION SOLO DEL TEXTO QUE DICE INGLES
ingles = parser.xpath("//a[@id='js-link-box-en']/strong/text()")
print(ingles[0])

# EXTRACCION DE TODOS LOS IDIOMAS POR CLASE
idiomas = parser.find_class('central-featured-lang')
for idioma in idiomas:
  print(idioma.text_content())

# EXTRACCION DE TODOS LOS IDIOMAS POR XPATH
idiomas = parser.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()")
for idioma in idiomas:
  print(idioma)
