import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import csv

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
response.encoding = 'utf-8'  # force le bon encodage
soup = BeautifulSoup(response.text, "html.parser")

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


#Récupération des datas de toutes les fonctions dans une liste
informations_book = [url, collect_UPC(), collect_price_including_tax(), collect_price_excluding_tax(), 
                    collect_availability(), collect_title(), collect_description(), collect_category(), 
                     collect_review_rating(), collect_image()]

#Création des en-têtes pour le fichier csv
en_tete = ['product_page_url','universal_ product_code (upc)', 'price_including_tax',
        'price_excluding_tax','number_available','title', 'product_description',
        'category', 'review_rating', 'image_url']

#Création du fichier csv 
with open("data.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(en_tete)
    writer.writerow(informations_book)


























#2 Test récupération information produit
"""informations_products = soup.find('table', class_='table table-striped')
dict_information_product = {}

for products in informations_products:
    if isinstance(products, Tag):
        dict_information_product[products.find('th').string] = products.find('td').string 

compteur = 0
list_information_product = [] 
for information in dict_information_product.values():
    compteur += 1
    print(f"Information numéro{compteur} : {information}")
    list_information_product.append(information)
print(list_information_product)

for element in list_information_product:
    print(element)"""




