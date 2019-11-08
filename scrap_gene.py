# coding=utf-8
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
from time import gmtime, strftime
import time as ti
import csv

# Récupération des url's depuis le fichier text
urls = [line.rstrip('\n') for line in open('./URLS.txt')]
instant = (strftime("%d-%m-%Y %H:%M:%S", gmtime()))
global_enveloppe = 1350000

# ouverture du tableau contenant le scrap
variables = pd.DataFrame(columns=['id', 'projet', 'secteur', 'porteur', 'enveloppe', 'votes'])

for url in urls:
    # Extraction des données et mise en soup
    result = requests.get(url)
    html_doc = result.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # construction des éléments de recherche.
    vote_html = soup.find('div', attrs={'class': 'stats'})

    # Récupération des données pour alimenter le tableau
    chain_id = soup.select_one('div.proposal-info > h1').text
    chain_id = chain_id.replace('N°',"")
    items = soup.select('div.row-content > p')
    chain_enveloppe = items[2]

    id = [int(i) for i in chain_id.split() if i.isdigit()][0]
    projet = url.split('/')[-1]
    secteur = items[0].get_text()
    enveloppe = [int(s) for s in chain_enveloppe.text.split() if s.isdigit()][0]
    porteur = items[3].get_text()
    votes = [int(s) for s in vote_html.text.split() if s.isdigit()][0]

    # Ajout d'une ligne
    new_row = pd.Series({"id": id, "projet": projet, "secteur": secteur, "porteur": porteur, "enveloppe": enveloppe, "votes": votes})
    print(new_row)
    variables = variables.append(new_row, ignore_index=True)

    ti.sleep(0.2)
    soup = ""

variables.sort_values(by=['votes'], ascending=False)


variables.to_csv("results_mdm2.csv", index=True, encoding='utf8')

print()
print(variables[variables.secteur == 'Mont-de-Marsan-2'])
print(variables.describe())
