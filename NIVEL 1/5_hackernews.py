"""
OBJETIVO: 
    - Solidificar los conocimientos de BeautifulSoup
    - Aprender otras técnicas para navegar por el árbol y obtener elementos en BeautifulSoup
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 05 AGOSTO 2023
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}

url = 'https://news.ycombinator.com/' # URL Semilla

# Hacemos el requerimiento a la web
respuesta = requests.get(url, headers=headers)

# Verificamos que obtenemos codigo 200
print(respuesta)

# Cargamos el arbol HTML en beautifoul soup
soup = BeautifulSoup(respuesta.text)

# Obtenemos todas las noticias
lista_de_noticias = soup.find_all('tr', class_="athing")

# Por cada noticia en la lista de noticias
for noticia in lista_de_noticias:
    # Obtenemos el titulo de la noticia
    titulo = noticia.find('span', class_='titleline').text

    # Obtenemos la URL a la que redirige al darle click a la noticia
    url = noticia.find('span', class_='titleline').find('a').get('href')

    # Puede ser que una noticia no tenga score o no tenga comentarios
    # Por lo que inicializaremos estos valores en 0
    score = 0
    comentarios = 0

    # La manera mas sencilla de obtener esta metadata es yendo al hermano siguiente
    # del titulo de la noticia
    metadata = noticia.find_next_sibling()

    try:
        score_tmp = metadata.find('span', class_='score').text
        score_tmp = score_tmp.replace('points', '').strip()
        score = int(score_tmp)
    except Exception as e:
        print(e)
        print('No se encontro score')

    try:
        # Para obtener el numero de comentarios, voy a obtener todo el subtitulo de la noticia
        subline = metadata.find(attrs={'class': 'subline'}).text
        # Y voy a hacer un manejo de cadenas de texto para obtener solo el numero de comentarios
        info = subline.split('|')
        comentarios_tmp = info[-1]
        comentarios_tmp = comentarios_tmp.replace('comments', '').strip()
        comentarios = int(comentarios_tmp)
    except:
        print('No se encontraron comentarios')

    print(titulo)
    print(url)
    print(score)
    print(comentarios)
    print()