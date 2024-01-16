import requests
import json
from lxml import html

headers = {
    "user-agent" : "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36 "
}

url = "https://footdistrict.com/adidas-ultra-boost-ltd-af5836.html"

session = requests.Session()

resp = session.get(url, headers=headers, allow_redirects=False)
print (resp)
print (resp.text)


# resp.encoding = 'utf-16'
# resp.encode('utf-16')
 
# parser = html.fromstring(resp.text, encoding = 'utf-8')

# print (resp.text)
 
# datos = parser.xpath('//script[contains(text(), "AEC.SUPER")]')

# print (datos)
 
# tallas = datos[0].text_content
 
# print(tallas)