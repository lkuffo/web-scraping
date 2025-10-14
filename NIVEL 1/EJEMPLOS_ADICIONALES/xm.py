import requests # pip install requests
from lxml import html # pip install lxml

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

# URL SEMILLA
url = 'https://www.xm.com.co/Paginas/Home.aspx'

# REQUERIMIENTO AL SERVIDOR. Esta pagina tiene un certificado desactualizado. Por lo que no 
# hacemos la verificacion de SSL al hacer el requerimiento
respuesta = requests.get(url, headers=headers, verify=False)

print (respuesta.text)