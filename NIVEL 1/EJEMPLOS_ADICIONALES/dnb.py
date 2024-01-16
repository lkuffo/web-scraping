import requests # pip install requests
from lxml import html # pip install lxml

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
}

# URL SEMILLA
url = 'https://www.dnb.com/business-directory/company-profiles.tubos_de_acero_de_m%C3%A9xico_sa.735c686c2d311a4222d52c9533ab8aee.html'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)
respuesta.encoding = 'UTF-8' # Codificar correctamente caracteres extranos

parser = html.fromstring(respuesta.text)

texto = parser.xpath("//div[@class='col-md-6 profile-heading-title']/text()")
print(texto[0])