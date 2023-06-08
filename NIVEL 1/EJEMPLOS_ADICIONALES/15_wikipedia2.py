import requests
from lxml import html
 
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}
 
url = "https://es.wikipedia.org/wiki/Web_scraping"
 
url_web = requests.get(url)
 
parser = html.fromstring(url_web.text)
 
secciones = parser.xpath("//li[contains(@class, 'toclevel-1')]")
for seccion in secciones:
  contenido = seccion.xpath(".//span/text()")
  indice = contenido[0]
  seccion = contenido[1]
  print (indice, seccion)
 