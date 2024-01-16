"""
OBJETIVO: 
    - Selenium en 2023: Objeto service y ChromeDriverManager
    - Selenium en Headless mode (sin navegador)
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ENERO 2024
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
#opts.add_argument("--headless") # Headless Mode

# Ahora podemos utilizar Selenium sin configurar el chromedriver (Julio 2023, Chrome > 115)
# Aunque en Mac esto tiene problemas
# driver = webdriver.Chrome(options=opts)

# Descarga automática del ChromeDriver
# Recomiendo esta forma de instanciar el ChromeDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

# Alternativamente:
# driver = webdriver.Chrome(
#     service=Service('./chromedriver'),
#     options=opts
# )

driver.get('https://www.airbnb.com/')

sleep(3)

titulos_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
for titulo in titulos_anuncios:
    print(titulo.text)