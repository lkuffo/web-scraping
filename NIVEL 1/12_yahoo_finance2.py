import pandas as pd
from bs4 import BeautifulSoup
import requests
 
headers = { 
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}
 
# Set up Driver
url = 'https://finance.yahoo.com/quote/AC.MX/history?p=AC.MX&guccounter=1'

# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)

# PARSEO DEL ARBOL CON BEAUTIFUL SOUP
soup = BeautifulSoup(respuesta.text)

data = [] # Lista que va a pasar a ser un dataframe

# Obtengo cada fila
for fila in soup.find_all('tr', {"class":"BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"}):
  info = [] # Aqui voy a poner la informacion de la fila
  # De cada fila obtengo cada celda
  for celda in fila.find_all('td'):
    info.append(celda.text) # Agrego cada celda a una lista
  try: # Manejo de errores
    AMC={ # Lleno un diccionario con la info
      "Date": info[0],
      "Open": info[1],
      "High": info[2],
      "Low": info[3],
      "Close": info[4],
      "Adj Close": info[5],
      "Volume": info[6]
    }
    data.append(AMC) # La agrego a mi lista de datos
  except:
    print('Error en fila', info)

# Convierto mi lista de datos a un dataframe
df = pd.DataFrame(data)
print (df)