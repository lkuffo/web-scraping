# Curso Maestro de Web Scraping en Python: Extracción de Datos de la Web

[ README IN CONSTRUCTION ]

![Photo](https://img-a.udemycdn.com/course/240x135/2861742_c063.jpg)

En este repositorio van a poder encontrar el código actualizado de las clases del curso maestro de Web Scraping. Conforme vayan cambiando las estructuras de las páginas este repositorio en lo posible se mantendrá actualizado.   

Adicional a esto, también se iran agregando los ejemplos adicionales propuestos por otros estudiantes en las preguntas del curso.    
   
## Content  
- **NIVEL 1**: SINGLE PAGES WITH REQUESTS Y SCRAPY    
- **NIVEL 2**: MANY PAGES WITH SCRAPY     
- **NIVEL 3**: AJAX LOADING (Dynamic Load) WITH SELENIUM       
- **NIVEL 4**: APIS & IFRAMES        
- **NIVEL 5**: AUTH & CAPTCHAS    
- **NIVEL EXTRA**: ALMACENAMIENTO, ACTUALIZACION Y AUTOMATIZACIÓN

| File | Website | Extraction Type | Tools Used | More Details  (Storage, Proxy, Auth,  Captcha or Automation) | Highlights |
|:-:|:-:|:-:|:-:|:-:|:-:|
| wikipedia.py | Wikipedia | Single Page | Requests lxml |  |  |
| stackoverflow_1.py | Stackoverflow | Single Page | Requests bs4 |  |  |
| stackoverflow_2.py | Stackoverflow | Single Page | Scrapy | Storage: csv/json |  |
| eluniverso.py | El Universo | Single Page | Scrapy bs4 | Storage: csv/json |  |
| sensacine.py | Sensacine | Single Page | Requests bs4 |  |  |
| luisaviaroma.py | Luis Viaroma | Single Page | Requests Session bs4 |  | - Doing two consecutive request to bypass anti-web scraping mechanism |
| footdistrict.py | Foot District | Single Page w/ AJAX Load | Requests bs4 |  | - Getting data from a JSON inside an script tag |
| xm.py |  | Single Page | Requests lxml |  | - Bad SSL Certificate Bypass |
| airbnb.py | Airbnb | Many Pages  (vertical crawling) | Scrapy CrawlSpider | Storage: csv/json | - OUTDATED |
| tripadvisor.py | TripAdvisor EC | Many Pages  (vertical crawling) | Scrapy CrawlSpider | Storage: csv/json | - Scrapy MapCompose to clean crawled data |
| mercadolibre.py | Mercado Libre EC | Many Pages  (vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json |  |
| ign.py | IGN Latam | Many Pages (vertical & N-dim horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json | - Many types of Scrapy items - OUTDATED |
| tripadvisor.py | TripAdvisor EC | Many Pages (2 levels of vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json |  |
| farmacia_cruzverde.py | Farmacia Cruz Verde | Many Pages (horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json | - Scrapy LinkExtractor parameters |
| urbania.py | Urbania | Many Pages (vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json Proxy: Crawlera | - Using CRAWLERA as Proxy in Scrapy - Configuring many start urls |
| tripadvisorperu.py | TripAdvisor PERU | Many Pages (vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json | - Filling items without an Item class in Scrapy |
| allocine.py | Allocine | Many Pages (vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json |  |
| dreamsparfurms.py | Dreams Parfums | Many Pages (vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json |  |
| mercadolibre_ven.py | Mercado Libre VEN | Many Pages (vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json |  |
| aliexpress.py | Ali Express | Single Page | Scrapy Spider |  |  |
| falabella.py | Falabella | Many Pages (vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json | - Scrapy LinkExtractor parameters |
| farmacia_ahumada.py | Farmcia Ahumada | Many Pages (horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json | - Running Scrapy without scrapy runspider command |
| tripadvisor_mx.py | Trip Advisor MX | Many Pages (2 levels of vertical & horizontal crawling) | Scrapy CrawlSpider | Storage: csv/json |  |
| cuevanaspider.py | Cuevana | Many Pages (vertical & horizontal crawling) | Scrapy CrawlSpider | Proxy: Custom | - Creating a custom Proxy for Scrapy |
| olx1.py | OLX Autos | Single Page w/ AJAX Load | Selenium WebDriver |  | - Clicking & Waiting on Selenium |
| olx2.py | OLX EC | Single Page w/ AJAX Load | Selenium WebDriver |  | - Waiting for DOM events on Selenium |
| mercadolibre.py | Mercado Libre EC | Many Pages  (vertical & horizontal crawling) | Selenium WebDriver |  | - Horizontal and Vertical Crawling in Selenium |
| googleplaces.py | Google Places | Single Page w/ AJAX Load | Selenium WebDriver |  | - Scrolling & Tabs management in Selenium |
| twitter.py | Twitter | Single Page w/ AJAX Load | Selenium WebDriver | Auth: Form Submit | - Filling forms in Selenium |
| farmaciajumbo.py |  | Single Page w/ AJAX Load | Selenium WebDriver |  |  |
| procuraduriacol.py |  | Single Page w/ AJAX Load | Selenium WebDriver | Captcha: Q&A | - Querying for information in a loop in Selenium |
| procuraduriacol2.py |  | Single Page w/ AJAX Load | Selenium WebDriver |  | - Querying for information in a loop in Selenium |
| olx_login.py | OLX  | Single Page w/ AJAX Load | Selenium WebDriver | Auth: Form submit |  |
| douglas.py |  | Single Page w/ AJAX Load | Selenium WebDriver |  |  |
| mitramiss.py |  | Single Page w/ AJAX Load | Selenium WebDriver | Files Extraction | - Download files by click in Selenium |
| douglas_df.py |  | Many Pages w/ AJAX Load (horizontal crawling)  | Selenium WebDriver | Storage: Pandas CSV | - Store information with Pandas and Selenium |
| turbosbwauto.py |  | Single Page w/ AJAX Load | Selenium WebDriver |  | - Managing Combo-boxes in Selenium |
| udemy.py | Udemy | Many API calls | Requests json | Storage: Pandas CSV |  |
| crunchyroll.py |  | Single Page | Requests lxml | Proxy: Custom | - Configuring custom proxy in Requests |
| ign_py | IGN LATAM | Single Page | Scrapy CrawlSpider |  | - iFrame extraction with Scrapy  - OUTDATED |
| mercantil.py |  | API call | Requests  |  | - Sending form-data with requests |
| w3s.py | W3S | Single Page | Scrapy CrawlSpider |  | - iFrame extraction with Scrapy |
| github.py | GitHub | Single Page after API call | Requests Session lxml | Auth: Form data submission | - Form-data login with requests |
| github2.py | GitHub | API call | Requests json | Auth: Basic | - Basic auth with requests |
| captchas.py | Google Examples | Single Page w/ AJAX Load | Selenium WebDriver | Captcha: reCAPTCHA v2 | - Solving Captchas manually  - Accessing inside iFrames in Selenium |
| captchas_auto.py | Google Examples | Single Page w/ AJAX Load | Selenium WebDriver | Captcha: reCAPTCHA v2 | - Solving Captchas with 2Captcha service |
| olx_images.py | OLX | Single Page w/ AJAX Load | Requests  Selenium WebDriver Pillow | Storage: File System Images Extraction | - Downloading images with Selenium & Requests |
| files_samples.py |  | Single Page | Requests bs4 | Storage: File System Files Extraction | - Downloading files with Requests & bs4 |
| mites_mongodb.py |  | Many Pages  (horizontal crawling) | Requests lxml | Storage: File System | - Downloading files from different pages in one extraction |
| scrapy_db_update_accuw.py | Accuweather | Many Pages (vertical crawling) | Scrapy CrawlSpider,  CrawlerRunner, LoopingCall Pymongo | Storage: MongoDB Automation: Every 20s | - Storing & Updating scraped data in MongoDB every 20 seconds (scrapy runner scheduling) |
| selenium_db_update_accuw.py | Accuweather | Many Pages (vertical crawling) | Selenium WebDriver Pymongo schedule | Storage: MongoDB Automation: Every 300s | - Storing & Updating scraped data in MongoDB every 5 minutes (python schedule) |
| olx_mongo.py | OLX | Single Page w/ AJAX Load | Selenium WebDriver Pymongo | Storage: MongoDB | - Storing scraped data in MongoDB |
| scrapy_automation_accuw.py | Accuweather | Many Pages  (vertical crawling) | Scrapy Crawlspider,  CrawlerRunner, LoopingCall | Storage: csv Automation: Every 20s | - Storing scraped data in a CSV file every 20 seconds (scrapy runner scheduling) |
| selenium_automation_accuw.py | Accuweather | Many Pages  (vertical crawling) | Selenium WebDriver | Storage: csv Automation: Every 60s | - Storing scraped data in a CSV file every 1 minute (python schedule) |


## Ayúdame con una donación:
Si sientes que el curso ha valido mucho más de lo que te ha costado, no dudes en hacerme una donación a través de PayPal. De esta forma me apoyas para hacer mas cursos y más contenido gratuito dentro de Youtube:   
💙 [Donación](https://paypal.me/leonardokuffo) 🧡   

## Encuéntrame también en:   
📹 [Youtube](https://www.youtube.com/channel/UCMqY16CUHOQvKepPW-f9M8Q)   
🐤 [Twitter](https://twitter.com/LeonardoKuffo)   
📷 [Instagram](https://www.instagram.com/leonardokuffo/)   
🎶 [Mi música en Spotify](https://open.spotify.com/artist/4SIr2DWV0Xx1uRQ04XkQJU)   
