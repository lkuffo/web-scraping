import requests
from lxml import html
from bs4 import BeautifulSoup

headers = {
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

# Abrimos una nueva sesion dentro de scrapy
session = requests.Session()

# Finalmente entro a la pagina donde quiero sacar la info estando autenticado gracias al session
data_url = 'https://github.com/lkuffo?tab=repositories'
respuesta = session.get(
  data_url, 
  headers=headers
)

parser = html.fromstring(respuesta.content)
repositorios = parser.xpath('//h3[@class="wb-break-all"]/a/text()')
for repositorio in repositorios:
  print (repositorio)