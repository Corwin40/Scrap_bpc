
#coding=utf-8

import requests
import re
from bs4 import BeautifulSoup


url = "https://budgetparticipatif.landes.fr/register"

result = requests.get(url)
html_doc = result.text
soup = BeautifulSoup(html_doc, 'html.parser')

# construction des éléments de recherche.
token = soup.find('input', attrs={'id': 'app_register_type__token'}).get('value')

s = requests.Session()

payload = {"app_register_type[email]":'argu.spri@gmail.com',
           'app_register_type[username]':'Titi40280',
           'app_register_type[plainPassword][first]':'Titi0604',
           'app_register_type[plainPassword][second]':'Titi0604',
           'app_register_type[profile][gender]':'m',
           'app_register_type[profile][firstname]':'Thierry',
           'app_register_type[profile][lastname]':'Filipowicz',
           'app_register_type[profile][phone]':'0558010203',
           'app_register_type[profile][address]':'212 chemin de larue',
           'app_register_type[profile][postcode]':'40000',
           'app_register_type[profile][date_of_birth][day]':'6',
           'app_register_type[profile][date_of_birth][month]':'4',
           'app_register_type[profile][date_of_birth][year]':'1968',
           'app_register_type[profile][customOptin]':'1',
           'app_register_type[cguOptin]':'1',
           'app_register_type[_token]':token
          }

s = requests.Session()
rpost = s.post(url, data=payload)

#print(rpost.text)
print(payload)
