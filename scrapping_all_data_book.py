import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import csv


#Récupération des URLS de toutes les catégories
def collecting_all_category():
    url_all_category = "https://books.toscrape.com/index.html"
    response_all_category = requests.get(url_all_category)
    response_all_category.encoding = 'utf-8'  # force le bon encodage
    if response_all_category.ok: #Vérification de la connexion à la page
        soup = BeautifulSoup(response_all_category.text, 'html.parser')

    all_category = soup.find('ul', class_="nav nav-list")
    collecting_all_category = all_category.find('ul')
    links_all_category = collecting_all_category.find_all('a')

    all_link = []

    for a in links_all_category:
        link = "https://books.toscrape.com/" + a['href']
        all_link.append(link)
        
    return all_link


#Récupération du nombre de page par catégorie
def total_of_page(url):
    response = requests.get(url)
    if response.ok: #Vérification de la connexion à la page
        soup = BeautifulSoup(response.text, 'html.parser')
    number_page = soup.find_all('ul', class_="pager")
    
    if number_page:
        for element in number_page:
            li = element.find('li', class_="current").get_text(strip=True)
            #L'arguement "strip" nous permet de contrôler la gestion des whitespaces et des newline characters
        return int(li[-1]) #Retourne le nombre de page présent pour la catégorie (dernier caractère de page "" of "" )
    else:
        return 1
    
def extraction_category_name(urls_category):
    all_urls_category_sans_index = []

    for url in all_urls_category:
        url_split = url.split("/")
        url_split.pop(-1)
        list_url_sans_index = ("/").join(url_split)
        all_urls_category_sans_index.append(list_url_sans_index)
        
    return all_urls_category_sans_index


#URLS de toutes les catégories
all_urls_category = collecting_all_category()

#URLS toutes catégories sans les "index.html"
all_urls_category_sans_index = extraction_category_name(all_urls_category)

#Création d'une liste pour récupérer les URL des livres par catégorie
list_all_url = []

#Création d'une liste pour récupérer les URL de toutes les catégories
list_all_category = []


#Boucle sur les URLS de toutes les catégories 
for urls in all_urls_category_sans_index:
    url_category = urls #Récupération de l'URL d'une des catégories
    list_all_category.append(url_category)
    
    
    #Récupération du nombre de page pour la catégorie
    number_of_page = total_of_page(url_category) 
    
    
    #Boucle pour récupérer les URLS des livres pour la catégorie choisie
    for i in range(number_of_page):
        if number_of_page > 1:
            url_category_page = f"{url_category}/page-{i+1}.html" #Suppression de "/index.html" remplacé par "/page-{i+1}.html"
            response = requests.get(url_category_page)
            response.encoding = 'utf-8'
            
            if response.ok: #Vérification de la connexion à la page
                soup_category = BeautifulSoup(response.text, 'html.parser')
                all_book_on_page = soup_category.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
                #Récupération des livres présents sur la page
                
                for book in all_book_on_page: #Récupération de chaque livre présent sur la page
                    a = book.find('a')
                    #print("URL du livre récupéré: ", url_category + a['href'])
                    list_all_url.append(url_category + a['href'])
                    
        else:
            response = requests.get(url_category)
            response.encoding = 'utf-8'
            
            if response.ok: #Vérification de la connexion à la page
                soup_category = BeautifulSoup(response.text, 'html.parser')
                all_book_on_page = soup_category.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3") 
                #Récupération des livres présents sur la page
                
                for book in all_book_on_page: #Récupération de chaque livre présent sur la page
                    a = book.find('a')
                    #print("URL du livre récupéré: ", url_category + a['href'])
                    list_all_url.append(url_category + a['href'])

print()
print("Nombre d'URL récupéré par catégorie: ", len(list_all_url))

with open("data_txt.txt", "w", newline="") as txt_file:
    for url in list_all_url:
        writer_txt = txt_file.write(f"{url}\n\n")



        
