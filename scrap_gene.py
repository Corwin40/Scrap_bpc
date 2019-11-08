# coding=utf-8
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
from time import gmtime, strftime

# Récupération des url's depuis le fichier text
urls = [line.rstrip('\n') for line in open('./URLS.txt')]
instant = (strftime("%d-%m-%Y %H:%M:%S", gmtime()))
global_enveloppe = 1350000

# ouverture du tableau contenant le scrap
variables = []

for url in urls:
    # Extraction des données et mise en soup
    result = requests.get(url)
    html_doc = result.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # construction des éléments de recherche.
    vote_html = soup.find('div', attrs={'class': 'stats'})

    # Récupération des données pour alimenter le tableau
    items = soup.select('div.row-content > p')
    chain_enveloppe = items[2]

    variable = {}
    variable['projet'] = url.split('/')[-1]
    variable['secteur'] = items[0].get_text()
    variable['enveloppe'] = [int(s) for s in chain_enveloppe.text.split() if s.isdigit()][0]
    variable['porteur'] = items[3].get_text()
    variable['vote'] = [int(s) for s in vote_html.text.split() if s.isdigit()][0]

    # Ajout d'une ligne
    variables.append(variable)

print(variables)


