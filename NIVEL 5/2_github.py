"""
OBJETIVO:  
    - Extraer los datos de repositorios publicos y privados de Github de mi cuenta.
    - Aprender a autenticarnos dentro de Requests utilizando Basic Auth.
    - Aprender a autenticarnos por medio de un API.
    - Contrastar la autenticacion por API y la autenticacion por FORM DATA (LOGIN).
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 09 ENERO 2023
"""
import requests

headers = {
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
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