"""
OBJETIVO:
    - Esta extracción es un codigo de ejemplo que no es funcional, para extraer todos los comentarios de
    - cada post. Esta extraccion no funciona debido a un fallo en la pagina de facebook que no permite
    - mostrar todos los comentarios. Tambien tiene el defecto de que utiliza muchos XPATHs que pueden
    - cambiar facilmente
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 14 ENE 2024
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Funcion para obtener el Script de Scrolling dependiendo de cuantos scrollings ya he hecho
# Es un approach mas inteligente que el utilizado en el video. En donde, mientras mas escrolls llevo dando, mas pixeles voy bajando.
# Simplemente remplazo el 20000 en la cadena del script, por un numero que dependa de la iteracion en que me encuentro actualmente
def obtener_script_scrolling(iteration): 
    scrollingScript = """ 
      window.scrollTo(0, 20000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
#opts.add_argument("--headless") # Headless Mode
# Agregar a todos sus scripts de selenium para que no aparezca la ventana de seleccionar navegador por defecto: (desde agosto 2024)
opts.add_argument("--disable-search-engine-choice-screen")

driver = webdriver.Chrome(options=opts)

# Vamos a la página de la cual queremos obtener los comentarios
driver.get('https://www.facebook.com/elcorteingles')
sleep(2)

# Cerramos el diálogo de cookies
boton_cookies = driver.find_element(By.XPATH, '//div[not(@aria-hidden)]/div[@aria-label="Allow all cookies"]')
boton_cookies.click()
sleep(0.5)

# Cerramos el diálogo que nos pida hacer Login
# Si necesitaramos hacer Login, tendriamos que llenar el formulario
cerrar_dialogo = driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@aria-label="Close"]')
cerrar_dialogo.click()
sleep(0.5)

# Creamos un conjunto de URLs (un conjunto nos permite almacenar elementos sin admitir repetidos)
# Primero vamos a almacenar todas las URLs de los posts, y luego accederemos a cada post
# Ventajas? Que si algo le pasa a la extracción, tendremos la lista completa de URLs
posts_urls = set([])

# La estrategia para la extracción de los posts será hacer scrolling tantas veces como sea necesaria
# para obtener al menos 50 posts. Con un máximo de 100 scrolls para evitar que se cuelgue infinitamente
# en caso de que no hayan suficientes posts
# Hay otras estrategias que también podriamos utilizar: 
#   1. Sabiendo que en cada scroll se cargan 3-4 posts. Podriamos dejarlo con un número definido de scrolls
#   2. Si al hacer 3 scrolls seguidos no se cargan nuevos posts, hacer un break
#   3. Si tuvieramos el número de posts en algún lado en la página; pudiéramos hacer scroll hasta estar cercanos a ese número
#      esto lo podriamos hacer por ejemplo en Youtube
n_scrolls = 0
max_scrolls = 100
while len(posts_urls) < 10 and n_scrolls < max_scrolls:
    contenedores = driver.find_elements(By.XPATH, '//span/a[@aria-label and contains(@href, "elcorteingles/posts")]') 
    for contenedor in contenedores:
        url = contenedor.get_attribute("href")
        posts_urls.add(url)

    driver.execute_script(obtener_script_scrolling(n_scrolls))
    n_scrolls += 1
    sleep(0.5)

# Idealmente guardariamos todas estas URLs en un archivo. De modo que si se cae la extracción en algun punto
# no tengamos que repetir el proceso de scrolling para obtener las URLs de los posts
print(posts_urls)

# Vamos a cada URL de cada post
for url in posts_urls:

    # Idealmente guardariamos esta URL en un archivo. De modo que si se cae la extracción en algun punto
    # sepamos de cuales URLs ya extrajimos datos y no las repitamos
    print(url)
    driver.get(url)
    sleep(2)

    # No nos interesa extraer datos de los posts que sean videos 
    # Tenemos que hacer esto porque la URL cambia al acceder a ella
    if "video" in driver.current_url:
        continue

    try:
        # Al acceder a una pagina nos puede volver a aparecer el dialogo
        cerrar_dialogo = driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@aria-label="Close"]')
        cerrar_dialogo.click()
        sleep(0.5)
    except:
        pass

    # Bajamos para que el anuncio de LOGIN no nos moleste al dar click
    driver.execute_script()

    # TODO: Aqui se cayo el codigo
    selector_tipo = driver.find_element(By.XPATH, "//span[text()='Most relevant']")
    selector_tipo.click()
    sleep(0.2)

    selector_todos = driver.find_element(By.XPATH, "//span[text()='All comments']")
    selector_todos.click()
    sleep(2)
    
    try:
        # Intentamos dar click en el boton para que se muestren todos los comentarios
        # Esta opcion solo aparece si hay cierto numero de comentarios
        ver_todos = driver.find_element(By.XPATH, "(//span[@class='x78zum5 x1w0mnb xeuugli']/span[starts-with(text(), 'View ')])[last()]")
        ver_todos.click()
        sleep(2)
    except:
        pass

    # Indexar en el primer elemento del resultado [1] es necesario debido a que 
    # puede haber un subpost al post
    texto_post = driver.find_element(By.XPATH, '(//div[@data-ad-comet-preview="message"])[1]').text

    reacciones = driver.find_element(By.XPATH, '//span[@class="xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk"]').text

    # Este mismo XPATH nos trae dos elementos; justamente el numero de comentarios
    # y el numero de compartidos, por lo tanto lo podemos indexar
    n_comentarios = driver.find_element(By.XPATH, '(//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn"])[1]').text
    compartidas = driver.find_element(By.XPATH, '(//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn"])[2]').text

    # El div es el contenedor de los comentarios
    # El ul/li es cada comentario individual en conjunto con las respuestas a ese comentario
    # Hacemos ademas un div[1] para solamente obtener el primer hijo del li, 
    # El cual es el comentario padre. Es decir, con div[1] ignoraremos las respuestas
    comentarios = driver.find_elements(By.XPATH, '//div[@class="x1jx94hy x12nagc"]/ul/li/div[1]')

    print()
    print(texto_post)
    print('Reacciones: ', reacciones)
    print('N Comentarios: ', n_comentarios) # Tambien lo podriamos sacar con len(comentarios)
    print('N compartidas: ', compartidas)
    print()
    
    # Por cada comentario que obtenemos
    for comentario in comentarios:
        try:
            # Intentaremos expandirlo si es posible
            ver_mas = comentario.find_element(By.XPATH, './/div[text()="See more"]')
            ver_mas.click()
            sleep(1)
        except:
            pass

        # Obtenemos el texto de dicho comentario
        # Mucho ojo con el ".", al inicio del xpath, esto hace una busqueda relativa al elemento y no en todo el arbol
        texto_comentario = comentario.find_element(By.XPATH, '.div[@role="dialog"]//span[@lang]//div[@dir="auto"]').text

        print(texto_comentario)
    
    # Opcional para ver si todo se realizó bien
    input()