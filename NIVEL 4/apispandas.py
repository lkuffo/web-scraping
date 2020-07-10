"""
OBJETIVO: 
    - Extraer nombre, reviews y rating de los cursos de Python.
    - Guardarlos en un CSV a traves de Pandas
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 10 JULIO 2020
"""
import requests
import pandas as pd

headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    "referer": "https://www.udemy.com/courses/search/?src=ukw&q=python",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

# Este lazo for me ayudara a iterar el parametro "page" del API
cursos_totales = []
for i in range (1, 2):
    # Esta URL, y los parametros la deciframos gracias al panel de Networks y a una tarea de investigacion
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?fields[locale]=simple_english_title&src=ukw&q=python&p=' + str(i)


    response = requests.get(url_api, headers=headers)

    # Parseo la respuesta en formato JSON. Requests automaticamente lo convierte en un diccionario de Python
    data = response.json()

    # Extraigo los datos del diccionario
    cursos = data["courses"]
    for curso in cursos:
        cursos_totales.append({
            "titulo": curso["title"],
            "num_reviews": curso["num_reviews"],
            "rating": curso["rating"]
        })


df = pd.DataFrame(cursos_totales)

print (df)

df.to_csv("cursos_udemy.csv")


