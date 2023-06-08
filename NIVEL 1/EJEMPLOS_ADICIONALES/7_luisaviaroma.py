import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}

# Primer requerimiento es una trampa para web scraping. 
url =  'https://www.luisaviaroma.com/es-es/p/nike/hombre/sneakers/70I-0M1001?ColorId=MDAx0&SubLine=shoes&CategoryId=97&lvrid=_p_d210_gm_c97&__s=MzgzODgxMQ'
# Al segundo requerimiento obtenemos la respuesta correcta
url2 = 'https://www.luisaviaroma.com/es-es/p/nike/hombre/sneakers/70I-0M1001?ColorId=MDAx0&SubLine=shoes&CategoryId=97&lvrid=_p_d210_gm_c97&__s=MzgzODgxMQ&aka_re=1'

# Abrimos una sesion en requests. Esto va a manejar los cookies
session = requests.Session()
# Primer requerimiento que setea los cookies y programa una redirección a la 2da URL.
respuesta = session.get(url, headers=headers) 

# Debido a que la redireccion no es ejecutada automaticamente, hacemos el requerimiento de manera manual a esta 2da URL, la cual es la misma URL que la original solamente con un &aka_re=1 al final.
respuesta = session.get(url2, headers=headers)

soup = BeautifulSoup(respuesta.text)
general = soup.find('div', id="allContainer")
print (general)

