"""
OBJETIVO: 
    - Hacer una extracción compleja en Selenium
    - Hacer una extracción de datos de una red social
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 13 ENERO 2024
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

# Funcion para obtener el Script de Scrolling dependiendo de cuantos scrollings ya he hecho
# Es un approach mas inteligente que el utilizado en el video. En donde, mientras mas escrolls llevo dando, mas pixeles voy bajando.
# Simplemente remplazo el 20000 en la cadena del script, por un numero que dependa de la iteracion en que me encuentro actualmente
def obtener_script_scrolling(iteration): 
    scrollingScript = """ 
      window.scrollTo(0, 20000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))


opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
#opts.add_argument("--headless") # Headless Mode

#driver = webdriver.Chrome(options=opts)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

driver.get('https://www.youtube.com/playlist?list=PLuaGRMrO-j-8NndtkHMA7Y_7798tdJWKH')
sleep(2)

# Disclaimer
boton_disclaimer = driver.find_element(By.XPATH, '//button[@aria-label="Accept all"]')
boton_disclaimer.click()
sleep(2)

videos = driver.find_elements(By.XPATH, '//div[@id="contents"]/ytd-playlist-video-renderer')
urls_videos = []
for video in videos:
    url = video.find_element(By.XPATH, './/h3/a[@id="video-title"]').get_attribute("href")
    urls_videos.append(url)

print(urls_videos)

# Vamos a cada video
for url in urls_videos:
    driver.get(url)
    sleep(3)

    # Hago un primer scrolling para que cargue el numero de comentarios
    driver.execute_script("""window.scrollTo(0, 400)""")
    sleep(3)

    # Obtengo cuantos comentarios hay en total segun youtube
    # Aproximo cuantos deberian de haber (ya que youtube oculta algunos)
    num_comentarios_totales = driver.find_element(By.XPATH, '//h2[@id="count"]//span[1]').text
    num_comentarios_totales = int(num_comentarios_totales) * 0.90
    print('Comentarios totales:', num_comentarios_totales)

    comentarios_cargados = len(driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]'))
    # Cada vez que hago scrolling voy a comparar si es que ya se encuentran cargados
    # todos los comentarios que youtube dice que hay 
    n_scrolls = 0
    n_scrolls_maximo = 10
    while comentarios_cargados < num_comentarios_totales and n_scrolls < n_scrolls_maximo:
        driver.execute_script(obtener_script_scrolling(n_scrolls))
        n_scrolls += 1
        sleep(2)
        comentarios_cargados = len(driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]'))        


    comentarios = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')
    for comentario in comentarios:
        texto_comentario = comentario.text
        print(texto_comentario)
    print()
    print()