import requests

from lxml import html


encabezados = {     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"

}

url = "https://www.wikipedia.org/" 



respuesta = requests.get(url, headers=encabezados) 



parser = html.fromstring(respuesta.text) 



ingles = parser.get_element_by_id("js-link-box-en")



print (ingles.text_content())