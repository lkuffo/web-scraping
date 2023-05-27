import requests
 
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# CREAMOS UN SESSION
session = requests.Session()

# LLENAMOS LOS COOKIES
url_madre = 'https://www.bolsadesantiago.com/'
response = session.get(url_madre, headers=headers)
print(response)

# OBTENEMOS EL TOKEN CSRF DE VALIDACION
url_token = 'https://www.bolsadesantiago.com/api/Securities/csrfToken'
response = session.get(url_token, headers=headers)
token = response.json()['csrf']
print(token)
headers['X-Csrf-Token'] = token # LO PONEMOS EN LOS HEADERS
 
# LLAMAMOS AL API FINALMENTE
url_api = 'https://www.bolsadesantiago.com/api/RV_ResumenMercado/getPresenciaBursatil'
response = session.post(url_api, headers=headers, data={"mercado": "AC", "bolsa": "TT", "fecha": "2023-05-22", "todas": "N"})
print(response)
print(response.text)
dicionario = response.json()
print(dicionario)