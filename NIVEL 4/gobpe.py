"""
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ENERO 2024
"""
import requests # pip install requests
from lxml import html # pip install lxml
import json

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
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