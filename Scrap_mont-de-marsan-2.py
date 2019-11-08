# coding=utf-8
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
from time import gmtime, strftime

# Récupération des url's depuis le fichier text
urls = [line.rstrip('\n') for line in open('./URLS.txt')]
data = pd.DataFrame(columns=['nom', 'secteur', 'porteur', 'enveloppe', 'votes'])
instant = (strftime("%d-%m-%Y %H:%M:%S", gmtime()))
global_enveloppe = 1350000

for url in urls:
    result = requests.get(url)

    # Extracts the response as html: html_doc
    html_doc = result.text

    # create a BeautifulSoup object from the HTML: soup
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Récupération des votes de l'url en cours.
    vote_html = soup.find('div', attrs={'class': 'stats'})
    vote = [int(s) for s in vote_html.text.split() if s.isdigit()][0]

    # Récupération des données pour alimenter le tableau
    Projet = url.split('/')[-1]
    items = soup.select('div.row-content > p')
    secteur = items[0].get_text()
    chain_enveloppe = items[2]
    enveloppe = [int(s) for s in chain_enveloppe.text.split() if s.isdigit()][0]
    porteur = items[3].get_text()

    # Ajout d'une ligne pour à la variable data[]
    new_row = pd.Series({"Projet": Projet, "secteur": secteur, "porteur": porteur, "enveloppe": enveloppe, "votes": vote})
    data = data.append(new_row, ignore_index=True)

data = data.sort_values(by=['votes'], ascending=False)
data = data.set_index('nom')

nbProjets = len(data)
sum_enveloppe = sum(data.enveloppe)

rang = data[data.secteur == 'Mont-de-Marsan-2'].index.get_loc('creer-un-espace-public-numerique')
classementGeneral = data.index.get_loc('creer-un-espace-public-numerique')
nosVotes = data.loc['creer-un-espace-public-numerique'].votes

# PARTIE TEST

# print(nom)

# PARTIE CODE RETOUR
print("Date et heure du scrap " + instant)
print("")
print(sum_enveloppe)
print("")
print("- - INFO GENERALES - - ")
print("Nombre total de projets : ", str(nbProjets))
#print("Enveloppe globale des demandes : " + all_enveloppe + " €")
print("")
print("- - RESULTATS PAR SECTEUR - - ")
print("Canton : " + secteur)

print(data[data.secteur == 'Mont-de-Marsan-2'])
print("")
print('Classement : ' + secteur + ': ', rang, ' / ', len(data[data.secteur == 'Mont-de-Marsan-2']))
print("")
print("Le projet d'espace numérique est classé ", str(classementGeneral), " / ", str(nbProjets),
      " avec ", str(nosVotes),
      " votes.")
