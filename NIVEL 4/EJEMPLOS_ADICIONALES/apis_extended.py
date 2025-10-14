"""
OBJETIVO: 
    - En este ejemplo propuesto por un estudiante combinamos una extraccion por APIs mas compleja a la cual
    le extendemos informacion con una siguiente extraccion utilizando cloudscraper (debido a que la pagina tiene verificacion de Javascript y Cloudflare)
    - La extraccion es informacion de cursos de udemy
ULTIMA VEZ EDITADO: 29 ABRIL 2024
"""
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep

import cloudscraper
 
def obtener_datos_curso(url_api, category, headers):
    cursos = []
    response = requests.get(url_api, headers=headers)
 
    data = response.json()
 
    paginacion = (data['unit']['pagination']['total_page'])
    for i in range(1, 2): 
        url_paginada = f"{url_api}&p={i}"
        response = requests.get(url_paginada, headers=headers)
        data = response.json()
        cursos_pagina = data["unit"]["items"]
        for curso in cursos_pagina: 
            try:
                titulo = curso["title"]
                descripcion = curso["headline"]
                duracion = curso["content_info"].replace(" total hours", "h").replace(" total hour", "h").replace(" total mins", "m")
                img = curso["image_480x270"]
                realease = curso["published_time"]
                realease_datatime = datetime.fromisoformat(realease)
                realease_format = realease_datatime.strftime("%m/%d/%Y")
                url = "https://deloittedevelopment.udemy.com" + curso["url"]
                url_navegador = "https://www.udemy.com/course/" + str(curso["id"])
 
                cursos.append({
                    'category': category,
                    'title': titulo,
                    'description': descripcion,
                    'duration': duracion,
                    'realease': realease_format,
                    'url_img': img,
                    'url': url,
                    'url_navegador': url_navegador
                })
            except Exception as e:
                print(e)
                pass
    return cursos
 
cursos = []
headers = {
    "Referer": "https://www.udemy.com/courses/search/?p=2&q=python&src=ukw",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
 
urls = [
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=338&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Business Operations'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=302&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Cloud Computing'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=342&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Communication'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=332&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Continuing Education Units'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=334&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Cybersecurity '),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=326&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Data Science'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=304&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Design Tools'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=306&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Development'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=308&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Finance & Accounting'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=312&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'IT Operations'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=336&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Language Learning'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=314&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Leadership & Management'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=316&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Marketing'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=320&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Personal Development'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=318&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Productivity'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=322&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Project & Product Management'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=324&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Sales & Customer Service'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=310&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'Workplace & Human Resources'),
    ('https://deloittedevelopment.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&subcategory=&instructional_level=&lang=en%7Ces&price=&duration=&closed_captions=&subs_filter_type=&sort=popularity&category_id=340&source_page=org_category_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat&', 'UX, Web & Mobile Design')
]
 
for url, category in urls:
    try:
        cursos.extend(obtener_datos_curso(url, category, headers))
    except Exception as e:
        print(e)
        pass


scraper = cloudscraper.create_scraper()

for curso in cursos:
    url_navegador = curso['url_navegador']

    resp = scraper.get(url_navegador, headers=headers)
    soup = BeautifulSoup(resp.text)
    descripcion = soup.find('div', {'data-purpose': "course-description"}).text
    print(descripcion)
    curso['descripcion_detallada'] = descripcion
    
with open('Udemy_test.json', 'w') as out_file:
    json.dump(cursos, out_file)