"""
OBJETIVO:
    - Hacer una extracción compleja en Selenium
    - Hacer una extracción de datos de una red social
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 14 ENERO 2023
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager


# Funcion para hacer un Scrolling SUAVIZADO dependiendo de cuantos scrollings ya he hecho
# Mientras mas escrolls llevo dando, mas pixeles voy bajando
# Para esto utilizo el scrolling que voy haciendo actualmente para bajar hasta cierta posicion en la pagina
def hacer_scrolling_suavizado(driver, iteracion):
    bajar_hasta = 2000 * (iteracion + 1)
    inicio = (iteracion * 2000) # Inicio donde termine la anterior iteracion
    for i in range(inicio,  bajar_hasta, 5): # Cada vez avanzo 5 pixeles
        scrollingScript = f""" 
          window.scrollTo(0, {i})
        """
        driver.execute_script(scrollingScript)


opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
# opts.add_argument("--headless") # Headless Mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# Vamos a la página de la cual queremos obtener los comentarios
driver.get('https://www.facebook.com/elcorteingles')
sleep(2)

# Cerramos el diálogo de cookies
boton_cookies = driver.find_element(By.XPATH, '//div[not(@aria-disabled) and @aria-label="Allow all cookies"]')
boton_cookies.click()
sleep(0.5)

# Cerramos el diálogo que nos pida hacer Login
# Si necesitaramos hacer Login, tendriamos que llenar el formulario
cerrar_dialogo = driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@aria-label="Close"]')
cerrar_dialogo.click()
sleep(0.5)

# La estrategia para la extracción de los posts será hacer scrolling tantas veces como sea necesaria
# para obtener al menos 50 posts. Con un máximo de 100 scrolls para evitar que se cuelgue infinitamente
# en caso de que no hayan suficientes posts
# Hay otras estrategias que también podriamos utilizar:
#   1. Sabiendo que en cada scroll se cargan 3-4 posts. Podriamos dejarlo con un número definido de scrolls
#   2. Si al hacer 3 scrolls seguidos no se cargan nuevos posts, hacer un break
#   3. Si tuvieramos el número de posts en algún lado en la página; pudiéramos hacer scroll hasta estar cercanos a ese número
#      esto lo podriamos hacer por ejemplo en Youtube
n_scrolls = 0
max_scrolls = 50
max_posts = 10
posts = driver.find_elements(By.XPATH, './/div[@aria-describedby and @role="article"]')
while len(posts) < max_posts and n_scrolls < max_scrolls:
    hacer_scrolling_suavizado(driver, n_scrolls)
    posts = driver.find_elements(By.XPATH, './/div[@aria-describedby and @role="article"]')
    n_scrolls += 1
    print('Termino scrolling: durmiendo')
    sleep(2)

posts = driver.find_elements(By.XPATH, './/div[@aria-describedby and @role="article"]')
for post in posts:
    # Indexar en el primer elemento del resultado [1] es necesario debido a que
    # puede haber un subpost al post
    texto_post = post.find_element(By.XPATH, '(.//div[@data-ad-comet-preview="message"])[1]').text

    url_post = post.find_element(By.XPATH, './/span[@id]//a[@aria-label]').get_attribute('href')

    # Este XPATH es unico dentro del post
    reacciones = post.find_element(By.XPATH, './/span[@class="x1e558r4"]').text

    # Traer los comentarios y compartidas es complicado debido a que comparten mismo XPATH
    # y debido a que podria existir solo uno de los dos, ambos, o ninguno
    n_comentarios = 0
    compartidas = 0

    # Asumimos que ambos existen y los traemos con un solo xpath
    comentarios_y_compartidas = post.find_elements(By.XPATH,'.//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"]')
    if len(comentarios_y_compartidas) == 2: # Si este XPATH nos trae dos elementos no hay problema
        n_comentarios = comentarios_y_compartidas[0].text
        compartidas = comentarios_y_compartidas[1].text
    elif len(comentarios_y_compartidas) == 0: # Si este XPATH no nos trae ningun elemento, ambos quedan en 0
        pass
    else: # Caso contrario tenemos que verificar cual de los dos existe, comentarios o compartidas
        # Si el post tiene un texto para ver mas comentarios, sabemos que comentarios debe existir
        texto_comentarios = post.find_elements(By.XPATH, './/span[text()="View more comments"]')
        hay_comentarios = len(texto_comentarios) > 0
        if hay_comentarios:
            n_comentarios = comentarios_y_compartidas[0].text
        else: # Caso contrario las compartidas son las que existen
            compartidas = comentarios_y_compartidas[0].text

    print()
    print(texto_post)
    print('Reacciones: ', reacciones)
    print('N Comentarios: ', n_comentarios)  # Tambien lo podriamos sacar con len(comentarios)
    print('N compartidas: ', compartidas)
    print('URL: ', url_post)
    print()