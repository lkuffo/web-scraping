from selenium import webdriver
from selenium.webdriver.common.by import By
'''from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait'''
from selenium.webdriver.chrome.options import Options
 
opts = Options()
opts.add_argument("--incognito")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', chrome_options=opts ) 
 
driver.get('https://www.pcprogramasymas.net/category/cursos/')
 
while True:  
    links_cursos = driver.find_elements(By.XPATH, '//div[@class="container"]//h2//a[1]')
    cursos_de_la_pagina = []
    for tag_a in links_cursos:
        cursos_de_la_pagina.append(tag_a.get_attribute("href"))
 
    for link in cursos_de_la_pagina:
        
        try:            
            driver.get(link)
            nombre = driver.find_element_by_xpath('//h2[@class="bc-title"]').text
            fecha = driver.find_element_by_xpath('//li[contains(text(), "2020")]').text
            peso = driver.find_element_by_xpath('//div[@class="blog-body"]//strong[contains(text(),"Peso")]').text
            contraseña = driver.find_element_by_xpath('//div[@class="blog-body"]//strong[contains(text(),"Contraseña")]').text
            enlacess = driver.find_elements_by_xpath('//div[@class="elementor-text-editor elementor-clearfix"]//a')
            enlaces_de_descarga = []
            for hilos in enlacess:
                try:
                    enlaces_de_descarga.append(hilos.get_attribute("href"))
                except Exception as e:
                    print(e)
                    driver.back()
                
            print(nombre)
            print(fecha)
            print(peso)
            print(contraseña)
            print(enlaces_de_descarga)
            
            print()
            
            driver.back()
 
        except Exception as e:
            print(e)
            driver.back()
    try:
        siguiente_pagina = driver.find_element_by_xpath('//ul[@class="pagination"]//li[@class="next"]')
        siguiente_pagina.click()
    except:
        break
        