import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import csv

def total_of_page():
    #Récupération du nombre de page total dans la catégorie
    url = f"https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-1.html"
    response = requests.get(url)
    if response.ok: #Vérification de la connexion à la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
    number_page = soup.find_all('ul', class_="pager")
    for element in number_page:
        li = element.find('li', class_="current").get_text(strip=True)
        #L'arguement "strip" nous permet de contrôler la gestion des whitespaces et des newline characters 
    return int(li[-1])


#Récupération des données par livre
def collect_title():
    title = soup.find('h1').string
    return title

def collect_price_including_tax():
    informations_products = soup.find('table', class_='table table-striped')

    for products in informations_products:
        if "<th>Price (incl. tax)</th>" in str(products.find('th')):
            return products.find('td').string
            

def collect_price_excluding_tax():
    informations_products = soup.find('table', class_='table table-striped')

    for products in informations_products:
        if "<th>Price (excl. tax)</th>" in str(products.find('th')):
            return products.find('td').string


def collect_UPC():
    informations_products = soup.find('table', class_='table table-striped')
    #print("Les informations produits récupérés sont: ",informations_products)
    
    for products in informations_products:
        if "<th>UPC</th>" in str(products.find('th')):
            return products.find('td').string


def collect_availability():
    informations_products = soup.find('table', class_='table table-striped')

    for products in informations_products:
        if "<th>Availability</th>" in str(products.find('th')):
            return products.find('td').string

def collect_description():
    product_page = soup.find('article', class_='product_page')
    list_element_product_page = []

    for element in product_page:
        list_element_product_page.append(element.get_text())
    
    return list_element_product_page[7]

def collect_category():
    category = soup.find_all('a')
    list_category = []
    
    for element in category:
        list_category.append(element.get_text())
    return list_category[-1]

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

def collect_image():
    image = soup.find('img') # Récupération de la balise img 
    image_url = image['src']
    return "https://books.toscrape.com/" + image_url


#Execution du code

number_of_page = total_of_page() #Récupération du nombre de page par catégorie

#Création d'une liste pour récupérer les URL des livres 
list_all_url = []
    
#Boucle pour récupérer les URLS des livres pour la catégorie choisie
for i in range(number_of_page):
    i += 1 
    url_category = f"https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-{i}.html"
    response = requests.get(url_category)
    response.encoding = 'utf-8'
    if response.ok: #Vérification de la connexion à la page
        soup_category = BeautifulSoup(response.text, 'html.parser')
        all_book_on_page = soup_category.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3") #Récupération des livres présents sur la page
        
        for book in all_book_on_page:
            a = book.find('a')
            list_all_url.append("https://books.toscrape.com/catalogue/category/books/historical-fiction_4/" + a['href'])
print("Nombre d'URL récupéré: ", len(list_all_url))



#Création du fichier CSV:

#Création de l'entête pour le fichier CSV
en_tete = ['product_page_url','universal_ product_code (upc)', 'price_including_tax',
    'price_excluding_tax','number_available','title', 'product_description',
    'category', 'review_rating', 'image_url']

#Initialisation d'un compteur à 0 pour analyse 
compteur = 0 

#Création du fichier CSV
with open("data.csv", "w", newline="") as csv_file:
    
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(en_tete) #Création de l'entête
    
    #Boucle pour analyser tous les URLS récupérés dans la catégorie choisie
    for book_url in list_all_url:
        compteur += 1
        print(f"URL {compteur} analysé: ",book_url)
        url = book_url 
        response_book = requests.get(url)
        response_book.encoding = 'utf-8'
        soup = BeautifulSoup(response_book.text, 'html.parser')
        
        #Création d'une liste contenant toutes les informations récupérées
        informations_book = [url, collect_UPC(), collect_price_including_tax(), collect_price_excluding_tax(), 
                        collect_availability(), collect_title(), collect_description(), collect_category(), 
                        collect_review_rating(), collect_image()]
        
        #Ecriture dans le fichier CSV
        print(f"Ecriture du fichier {compteur}")
        writer.writerow(informations_book)



