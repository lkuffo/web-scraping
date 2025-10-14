import requests
from bs4 import BeautifulSoup
 
server = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
 
url = "http://www.sensacine.com/empresa/ficha-23308/actividad-8030/"
 
respuesta = requests.get(url, headers = server)
 
parseador = BeautifulSoup(respuesta.text)
 
peliculas = parseador.find_all('div', class_="meta")
 
for pelicula in peliculas:
    texto_titulo = pelicula.find(class_="meta-title-link").text
    fecha = pelicula.find(class_='date').text
 
    print(texto_titulo)
    print(fecha)
 
    print()