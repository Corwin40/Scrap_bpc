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
limit_enveloppe = 1500000
cumul_enveloppe = 0
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
    variables = variables.append(new_row, ignore_index=True)

    # Addition des enveloppes
    cumul_enveloppe = cumul_enveloppe + enveloppe
    print(cumul_enveloppe)

variables = variables.sort_values(by=['votes'], ascending=False)
variables = variables.set_index('projet')

nbprojet = len(variables)
nbprojet_secteur = len(variables[variables.secteur == "Mont-de-Marsan-2"])

sum_secteur = sum(variables[variables.secteur == "Mont-de-Marsan-2"].enveloppe)

nosVotes = variables.loc['creer-un-espace-public-numerique'].votes
classement_gene = variables.index.get_loc('creer-un-espace-public-numerique') + 1
classement_secteur = variables[variables.secteur == 'Mont-de-Marsan-2'].index.get_loc('creer-un-espace-public-numerique') + 1

# PARTIE CODE RETOUR
print("Date et heure du scrap " + instant)
print("")
print("- - INFO GENERALES - - ")
print("Nombre total de projets : ", str(nbprojet))
print("enveloppe globale des projets sélectionnés : ", sum(variables.enveloppe), "€")
print("")
print("- - RESULTATS SECTEUR : Mont de Marsan 2 - - ")
print("Nombre total de projets : ", str(nbprojet_secteur))
print("enveloppe des projets : ", sum_secteur, "€")
print("Nombre de vote : ", nosVotes)
print("Le projet est classé au global : ", str(classement_gene), " / ", str(nbprojet), " avec ", str(nosVotes), " votes.")
print("Le projet est classé : ", str(classement_secteur), " / ", str(nbprojet_secteur), " avec ", str(nosVotes)," votes.")
print("- - TABLEAU - - ")
print(variables)

variables[variables.secteur == 'Mont-de-Marsan-2'].to_csv("results_mdm2.csv", index=True, encoding='utf8')