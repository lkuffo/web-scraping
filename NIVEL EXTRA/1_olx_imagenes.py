"""
OBJETIVO:  
    - Descargar las imagenes de los anuncios de OLX.
    - Aprender a descargar imagenes de la web a nuestra pc.
    - Aprender una segunda manera para hacer scrolling de una pagina web.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 02 ENERO 2024
"""
import requests
from PIL import Image # pip install Pillow
import io
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# Agregar a todos sus scripts de selenium para que no aparezca la ventana de seleccionar navegador por defecto: (desde agosto 2024)
opts.add_argument("--disable-search-engine-choice-screen")

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)

# Voy a la pagina que requiero
driver.get('https://www.olx.in')

sleep(3) # Soluciona bug extrano en OLX

for i in range(1): # Voy a darle click en cargar mas 3 veces
    try:
        # Busco el boton para cargar mas informacion
        boton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        # le doy click
        boton.click()
        # espero que cargue la informacion dinamica
        WebDriverWait(driver, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )

    except:
        # si hay algun error, rompo el lazo. No me complico.
        break

# Las imagenes solo son cargadas cuando se encuentran dentro del paneo visual del usuario
# Por lo tanto ejecuto un script de scrolling "smooth", que hara scrolling lentamente
# Hasta el comienzo de la pagina
driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
sleep(5)
# Para asegurarme que todas las imagenes han sido cargadas, hago un scrolling hasta 
# bien abajo en la pagina (20mil pixeles, podria necesitar mas pixeles eventualmente)
driver.execute_script("window.scrollTo({top: 20000, behavior: 'smooth'});")
sleep(5)


# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
anuncios = driver.find_elements('xpath', '//li[@data-aut-id="itemBox"]')

i = 0
# Recorro cada uno de los anuncios que he encontrado
for anuncio in anuncios:
    # print(anuncio.get_attribute('innerHTML'))
    # Por cada anuncio hallo el preico
    precio = anuncio.find_element('xpath', './/span[@data-aut-id="itemPrice"]').text
    print (precio)
    # Por cada anuncio hallo la descripcion
    descripcion = anuncio.find_element('xpath', './/span[@data-aut-id="itemTitle"]').text
    print (descripcion)

    try:
        url = anuncio.find_element('xpath', './/figure[@data-aut-id="itemImage"]/img')
        # obtengo el URl de la imagen del anuncio
        url = url.get_attribute('src')
        
        # con requests, hago el requerimiento a la URL de la imagen
        # Es importante aqui no olvidar los principios que hemos aprendido en el curso,
        # y pasar headers con un user-agent
        image_content = requests.get(url, headers=headers).content

        # PROCESAMIENTO DE LA IMAGEN
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = './imagenes/'+ str(i) + '.jpg'  # nombre a guardar de la imagen
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
    except Exception as e:
        print(e)
        print ("Error")
    i += 1