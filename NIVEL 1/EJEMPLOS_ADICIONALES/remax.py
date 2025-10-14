from bs4 import BeautifulSoup
import requests
 
headers = { 
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}
 
# Set up Driver
url = 'https://www.remax.bo/es-bo/propiedades/terreno/en-venta/cochabamba/av-9-de-abril-cercado-cbba-av-9-de-abril-y-calle-e-soruco/120032009-45?LFPNNSource=RecentlyListedOfficeProperties&cKey=120032009-45'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)

# PARSEO DEL ARBOL CON BEAUTIFUL SOUP
soup = BeautifulSoup(respuesta.text)


script = soup.find('div', class_="googlemap-office").find('script', type="text/javascript")

print (script.text)