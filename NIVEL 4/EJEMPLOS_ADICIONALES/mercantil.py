import requests
 
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "content-type": "application/json; charset=UTF-8" # ESTA ES EL UNICO HEADER IMPORTANTE
}

url_api = "https://www.mercantil.com/rubro.aspx/GetSelCompanies"

response = requests.post(
    url_api, 
    headers=headers, 
    data='{"Acti_Code":"1798","Country":1,"Lang":"esp","Sort":"","Filter":"","Branch":"","OnlyWeb":"","Str_Comuna":"","Str_City":"","Str_Region":""}'
)

diccionario = response.json()
print (len(diccionario['d']))
#print(response.json()) # Imprimir esta linea puede colgar tu PC. Es muy grande el diccionario