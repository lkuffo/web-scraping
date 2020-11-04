import requests
import pandas as pd
headers={"USER_AGENT":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36",
         "origin":"https://www.premierleague.com"}
equipos_totales=[]
 
for i in range(0,2):
  url_api='http://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=42&teams=1,2,127,4,6,7,26,10,11,12,23,14,20,42,29,45,21,33,36,25&pageSize=40&sort=desc&statuses=C&altIds=true&page='+ str(i)
  response=requests.get(url_api,headers=headers)
  data=response.json()
  equipos = datos["entity"]["teams"]
  id_equipo1 = equipos[0]["id"] # Obtengo el id de los equipos
  id_equipo2 = equipos[1]["id"]
  
  info_eq1 = datos["data"][id_equipo1]["M"] # uso el id que obtengo para buscar los datos del equipo
  info_eq2 = datos["data"][id_equipo2]["M"]
  
  info_a_buscar = "aerial_won" # nombre de la info que quiero buscar
  
  # Recorro cada una de las listas que tiene toda la informacion, para poder buscar la informacion que quiero, en este caso duelos aereos
  
  for info in info_eq1: # por cada diccionario de la lista de informacion
      if info["name"] == info_a_buscar: # pregunto si ese diccionario contiene en su clave name la info que quiero buscar
          duelos_aereos_eq1 = info["value"] # en ese caso guardo mi variable
  
  # hago lo mismo para el equipo2
  for info in info_eq2:
      if info["name"] == info_a_buscar:
          duelos_aereos_eq1 = info["value"]

df=pd.DataFrame(equipos_totales)
print(df)
df.to_csv("scores3.csv")