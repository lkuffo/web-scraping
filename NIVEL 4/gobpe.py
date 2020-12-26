import requests # pip install requests
from lxml import html # pip install lxml
import json

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

# URL SEMILLA

for i in range(1, 5):
    url = "https://www.gob.pe/busquedas?contenido[]=normas&institucion[]=mininter&reason=sheet&sheet=" + str(i) + "&term=renuncia"

    # REQUERIMIENTO AL SERVIDOR
    respuesta = requests.get(url, headers=headers)

    # PARSEO DEL ARBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
    parser = html.fromstring(respuesta.text)

    # EXTRACCION SOLO DEL TEXTO QUE DICE INGLES
    datos = parser.xpath("//script[contains(text(), 'window.initialData')]")
    datos = datos[0].text_content()
    indice_ini = datos.find('{')

    datos = datos[indice_ini:]
    objeto = json.loads(datos)
    for resultado in objeto['data']['attributes']['results']:
        print(resultado["content"])