import requests
import pandas as pd

headers={
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36",
    "origin":"https://www.premierleague.com"
}

url_api='https://footballapi.pulselive.com/football/stats/match/12494'
response=requests.get(url_api,headers=headers)
datos=response.json()
equipos = datos["entity"]["teams"]

id_equipo1 = str(equipos[0]["team"]["id"]) # Obtengo el id de los equipos
nombre_equipo1 = str(equipos[0]["team"]["name"])
id_equipo2 = str(equipos[1]["team"]["id"])
nombre_equipo2 = str(equipos[1]["team"]["name"])

info_eq1 = datos["data"][id_equipo1]["M"] # uso el id que obtengo para buscar los datos del equipo
info_eq2 = datos["data"][id_equipo2]["M"]

info_a_buscar = "possession_percentage" # nombre de la info que quiero buscar

# Recorro cada una de las listas que tiene toda la informacion, para poder buscar la informacion que quiero, en este caso duelos aereos

for info in info_eq1: # por cada diccionario de la lista de informacion
    if info["name"] == info_a_buscar: # pregunto si ese diccionario contiene en su clave name la info que quiero buscar
        duelos_aereos_eq1 = info["value"] # en ese caso guardo mi variable
        print (nombre_equipo1, duelos_aereos_eq1)

# hago lo mismo para el equipo2
for info in info_eq2:
    if info["name"] == info_a_buscar:
        duelos_aereos_eq2 = info["value"]
        print (nombre_equipo2, duelos_aereos_eq2)
