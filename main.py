import json
import requests
from fake_headers import Headers
from pprint import pprint
from bs4 import BeautifulSoup
import unicodedata

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser='chrome', os='win')

links_list = []
vacancy_list = []
vac_links = []
salary_list = []
company_name_list = []
city_list = []
final_list = []

def links():
    vacancies = (BeautifulSoup(requests.get(url, headers=headers.generate()).text, features='lxml')).find_all('a', class_="serp-item__title")
    for vacancy in vacancies:
        links = vacancy['href']
        links_list.append(links)
        descr = (BeautifulSoup(requests.get(links, headers=headers.generate()).text, features='lxml')).find('div', {
            'data-qa': 'vacancy-description'})
        if not descr:
            continue
        if ('Django' or 'django' or 'Flask' or 'flask') in descr.text:
            vacancy_list.append('yes')
        else:
            vacancy_list.append('no')
    for l, v in zip(links_list, vacancy_list):
        if v == 'yes':
            vac_links.append(l)
    return vac_links

def salaries():
    for link in vac_links:
        salary = (BeautifulSoup(requests.get(link, headers=headers.generate()).text, features='lxml')).find('span', class_="bloko-header-section-3")
        if not salary:
            continue
        salary_list.append(unicodedata.normalize('NFKD', salary.text))
    return salary_list

def company_names():
    for link in vac_links:
        company_name_link = (BeautifulSoup(requests.get(link, headers=headers.generate()).text, features='lxml')).find('a', class_="bloko-link bloko-link_kind-tertiary")
        if not company_name_link:
            continue
        company_name = company_name_link['href']
        company_name_2 = (BeautifulSoup(requests.get(f'https://spb.hh.ru{company_name}', headers=headers.generate()).text, features='lxml')).find('span', class_="company-header-title-name")
        if not company_name_2:
            continue
        company_name_list.append(unicodedata.normalize('NFKD', company_name_2.text))
    return company_name_list

def cities():
    for link in vac_links:
        city = (BeautifulSoup(requests.get(link, headers=headers.generate()).text, features='lxml')).find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
        if not city:
            continue
        city_list.append(city.text)
    return city_list

def res(link, salary, company_name, city):
    result = zip(link, salary, company_name, city)
    for link, salary, company_name, city in result:
        res_dict = {'link': link,
                    'salary': salary,
                    'company_name': company_name,
                    'city': city}
        final_list.append(res_dict)
    return final_list


links()
salaries()
company_names()
cities()
res(vac_links, salary_list, company_name_list, city_list)

with open('data.json','w', encoding='utf-8') as f:
    json.dump(final_list, f, indent=1, ensure_ascii=False)





