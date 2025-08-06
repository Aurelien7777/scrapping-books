import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import csv
from urllib.parse import urljoin
from urllib.parse import urlparse
import urllib.request
import os


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
    
#Extraction de l'URL sans le index.html
def extraction_url_without_index(urls_category):
    all_urls_category_sans_index = []

    for url in all_urls_category:
        url_split = url.split("/")
        url_split.pop(-1)
        list_url_sans_index = ("/").join(url_split)
        all_urls_category_sans_index.append(list_url_sans_index)
        
    return all_urls_category_sans_index

#Extraction du nom de la catégorie
def extraction_category_name(urls_category):
    all_category_name = []

    for url in all_urls_category:
        url_split = url.split("/")
        category_name = url_split[-2]
        all_category_name.append(category_name)
    
    return all_category_name



#RECUPERATION DES INFORMATIONS POUR LES LIVRES

#Récupération du titre du produit
def collect_title():
    title = soup.find('h1').string
    return title

#Récupération du prix incluant les taxes
def collect_price_including_tax():
    informations_products = soup.find('table', class_='table table-striped')

    for products in informations_products:
        if "<th>Price (incl. tax)</th>" in str(products.find('th')):
            return products.find('td').string
            
#Récupération du prix excluant les taxes
def collect_price_excluding_tax():
    informations_products = soup.find('table', class_='table table-striped')

    for products in informations_products:
        if "<th>Price (excl. tax)</th>" in str(products.find('th')):
            return products.find('td').string

#Récupération du code universel du livre
def collect_UPC():
    informations_products = soup.find('table', class_='table table-striped')
    
    for products in informations_products:
        if "<th>UPC</th>" in str(products.find('th')):
            return products.find('td').string

#Récupération du nombre de livre disponible 
def collect_availability():
    informations_products = soup.find('table', class_='table table-striped')

    for products in informations_products:
        if "<th>Availability</th>" in str(products.find('th')):
            return products.find('td').string
        
#Récupération de la description du livre
def collect_description():
    product_page = soup.find('article', class_='product_page')
    list_element_product_page = []

    for element in product_page:
        list_element_product_page.append(element.get_text())
    
    return list_element_product_page[7]

#Récupération de la catégorie du livre
def collect_category():
    category = soup.find_all('a')
    list_category = []
    
    for element in category:
        list_category.append(element.get_text())
    return list_category[-1]

#Récupération de la note du livre
def collect_review_rating():
    dict_star_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
    all_p = soup.find_all('p') # Itération sur tous les paragraphes
    paragraphe_review = all_p[2] # Récupération du paragraphe contenant les avis
        
    class_star_rating = paragraphe_review.attrs.values() 
    # Utilisation de attrs.values() car la variable est de type dictionnaire 
    # pour la récupération des valeurs du dictionnaire "Star-rating" et three"
    list_star_rating = list(class_star_rating) #Conversion en liste
    liste_initial = list_star_rating[0] # Récupération d'une des 2 listes imbriquées/Conversion en une seule liste
    star_rating = liste_initial[-1] # Récupération du nombre d'étoile

    for values in dict_star_rating: # Boucle dans le dictionnaire pour convertir le "str" en "int"
        if star_rating == values:
            star_rating = dict_star_rating[values]
    return str(star_rating)

#Récupération de l'image du livre
def collect_image():
    image = soup.find('img') # Récupération de la balise img 
    image_url = image['src']
    return urljoin("https://books.toscrape.com/", image_url)





#PARTIE EXECUTION DU CODE

#URLS de toutes les catégories
all_urls_category = collecting_all_category()

#URLS toutes catégories sans les "index.html"
all_urls_category_sans_index = extraction_url_without_index(all_urls_category)

#Noms de toutes les catégorie sous forme de liste
all_category_name = extraction_category_name(all_urls_category)

#Création d'une liste pour récupérer les URL de toutes les catégories
list_all_category = []

#Création d'une liste pour récupérer les URL des livres par catégorie
list_all_url = []

#Création d'une liste pour récupérer les images des livres
list_all_images = []

#Création des en-têtes pour le fichier csv
header = ['product_page_url','universal_ product_code (upc)', 'price_including_tax',
        'price_excluding_tax','number_available','title', 'product_description',
        'category', 'review_rating', 'image_url']


#Initialisation d'un compteur pour les index de la liste des noms de catégorie
compteur = 0

#Création du dossier "COLLECT_DATA"
os.makedirs("COLLECT_DATA", exist_ok=True)
print("Création du dossier COLLECT DATA effectué")

#Boucle sur les URLS de toutes les catégories sans le "index.html"
for urls in all_urls_category_sans_index:
    url_category = urls #Récupération de l'URL d'une des catégories
    list_all_category.append(url_category)
    
    #Création d'un dossier image pour chaque catégorie
    folder = f"IMAGE_CATEGORY_{all_category_name[compteur]}"
    os.makedirs(folder, exist_ok=True)
    print(f"Création du dossier image pour la catégorie {all_category_name[compteur]}")
    
    #Création du fichier CSV pour la catégorie
    with open(f"COLLECT_DATA\data_book_category_{all_category_name[compteur]}.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file) #Creation de l'objet "writer"
        writer.writerow(header)
        
        #Incrémentation du compteur
        compteur += 1 
        
        #Récupération du nombre de page pour la catégorie choisie
        number_of_page = total_of_page(url_category) 

        print("Phase de récupération d'URL des livres pour la catégorie choisie..")
        #Boucle pour récupérer les URLS des livres pour la catégorie choisie
        for i in range(number_of_page):
            #Si le nombre de page dans la catérogie est supérieur à 1
            if number_of_page > 1:
                url_category_page = f"{url_category}/page-{i+1}.html" #Suppression de "/index.html" remplacé par "/page-{i+1}.html"
                response = requests.get(url_category_page)
                response.encoding = 'utf-8'
            else:
                #Si le nombre de page de la catégorie est égal à 1
                url_category_page = url_category
                response = requests.get(url_category)
                response.encoding = 'utf-8'
                
            if response.ok: #Vérification de la connexion à la page
                
                print("Récupération URL des livres pour la catégorie effectuée!")
                soup_category = BeautifulSoup(response.text, 'html.parser')
                #Récupération de tous les livres présents sur la page
                all_book_on_page = soup_category.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
                
                print("Phase de récupération des livres présents dans la catégorie en cours..")
                #Récupération de chaque livre présent sur la page
                for book in all_book_on_page: 
                    a = book.find('a')
                    list_all_url.append(url_category + a['href'])
                    
                    #Extraction du nom de la catégorie et de "index.html" pour la construction de l'URL book
                    href = a['href']
                    href_split = href.split("/")
                    book_name = href_split[-2]
                    index = href_split[-1]
                    
                    #Reqûete pour récupération des informations pour chaque livre dans la catégorie
                    url_book = f"https://books.toscrape.com/catalogue/{book_name}/{index}"
                    #print("L'URL récupéré est: ",url_book)
                    response_book = requests.get(url_book)
                    response_book.encoding = 'utf-8'  # force le bon encodage
                    
                    #Vérification de la requête
                    if response_book.ok:
                        soup = BeautifulSoup(response_book.text, "html.parser")
                        
                        #Récupération des datas de toutes les fonctions dans une liste
                        informations_book = [url_book, collect_UPC(), collect_price_including_tax(), collect_price_excluding_tax(), 
                                            collect_availability(), collect_title(), collect_description(), collect_category(), 
                                            collect_review_rating(), collect_image()]
                        
                        #Ecriture des information dans le fichier
                        writer.writerow(informations_book) 
                        
                        #Ajout de l'image dans la liste des images
                        image_url = collect_image()
                        #print("L'image récupérée est: ", image_url)                           
                        list_all_images.append(image_url)
                        
                        
                        #Récupération et Création des fichiers images                           
                        filename = os.path.basename(image_url) #"filename" extrait le nom du fichier depuis l’URL avec os.path.basename(image).
                        filename = f"image_{book_name}.jpg"
                        with urllib.request.urlopen(image_url) as url: #Téléchargement de l'image
                            image_data = url.read() #Lit les données de l’image.
                            
                        # Enregistre le contenu de l'image dans un fichier
                        file_path = f"{folder}/{filename}"
                        with open(file_path, "wb") as f: #Crée un fichier local avec le nom extrait.
                            f.write(image_data) #Écrit les données de l’image dans ce fichier en mode binaire ("wb").
                    else:
                        print("ERREUR! La connexion est impossible")


print("Nombre total d'URL récupérés de livre récupérés: ", len(list_all_url))
print("Nombre d'URL de catégorie récupérés: ", len(list_all_category))
print("Nombre total d'URL images récupérés: ", len(list_all_images))

