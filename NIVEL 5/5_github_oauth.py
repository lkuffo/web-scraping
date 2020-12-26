"""
OBJETIVO:  
    - Aprender a autenticarnos dentro de Requests utilizando OAUTH.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 26 DICIEMBRE 2020
"""
import requests

headers = {
  "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

# Documentacion del API: https://api.github.com/
endpoint = 'https://api.github.com/user/repos?page=3'

password = open('./oauthtoken.txt').readline().strip()
response = requests.get(
  endpoint, 
  headers=headers, 
  auth=('lkuffo', password) # TUPLA DE AUTENTICACION POR MEDIO DE BASIC AUTH
)

# RESPUESTA ESTA EN FORMATO JSON
repositorios = response.json() # puedo utilizar la libreria json como en la clase, para verla mejor
for repositorio in repositorios:
  print (repositorio["name"])