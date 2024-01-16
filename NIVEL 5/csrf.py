"""
OBJETIVO: 
    - Aprender a afrontarnos a una extracción con complejidad elevada
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ENERO 2024
"""

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# CREAMOS UN SESSION
session = requests.Session()

response = session.get('https://www.bolsadesantiago.com/', headers=headers)
print(response)

# OBTENER EL TOKEN CSRF CON EL API
url_token = 'https://www.bolsadesantiago.com/api/Securities/csrfToken'
response = session.get(url_token, headers=headers)
print(response.text)
token = response.json()['csrf']
print(token)

headers['X-Csrf-Token'] = token

# LLAMAMOS AL API
url_api = 'https://www.bolsadesantiago.com/api/Comunes/getHoraMercado'

response = session.post(url_api, headers=headers)

print(response)
# print(response.text)
#
dicionario = response.json()
print(dicionario)