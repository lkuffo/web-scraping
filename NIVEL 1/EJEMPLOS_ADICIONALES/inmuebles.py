import requests
from lxml import html
import json
 
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}
 
url = "https://propiedades.com/inmuebles/casa-en-venta-zona-2-fraccion-4-dzitya-yucatan-18809109"
 
resp = requests.get(url, headers=headers)
parser = html.fromstring(resp.text)
 
datos = parser.xpath("//script[contains(text(),'calculator_property')]")
 
texto_script = datos[0].text_content()
 
print (texto_script)