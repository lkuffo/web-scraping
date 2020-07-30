import requests
from lxml import html
 
 
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}
 
url_semilla = 'https://www.crunchyroll.com/es-es/login'
 
sesion =requests.session()

proxyDict = { 
              # "http"  : "http://45.70.201.52:999", 
              "https" : "https://200.89.159.153:8080"
            }

login_respuesta = sesion.get(url_semilla, headers=headers, proxies=proxyDict)

print (login_respuesta.text)
 
parser = html.fromstring(login_respuesta.text)
token_especial = parser.xpath('//input[@name="login_form[_token]"]/@value')
 
print(token_especial)