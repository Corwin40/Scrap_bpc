import requests
from bs4 import BeautifulSoup

with open('./URLS.txt', 'w') as out_file:
    for i in range(1, 42):
        print("Récupération des urls de la page ", str(i), " sur 41")
        # url of page y is of type .....?page=y
        url = 'https://budgetparticipatif.landes.fr/dialog/budget-participatif-2019?orderby=alphabetical&page=' + str(i)
        # get page
        result = requests.get(url)
        # Extracts the response as html: html_doc
        html_doc = result.text
        # create a BeautifulSoup object from the HTML: soup
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Find all 'a' tags (which define hyperlinks): a_tags
        a_tags = soup.find_all('a', attrs={'class': 'proposal-link'})
        # save urls in text file
        for link in a_tags:
            out_file.write('https:'+link.get('href')+'\n')
