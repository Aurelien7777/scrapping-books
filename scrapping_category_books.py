import requests
from bs4 import BeautifulSoup
import scrapping_books

#Récupération des URL des livres 
def collect_books_name(total_page):
    list_all_url = []
    
    for i in range(total_page):
        i += 1 
        url = f"https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-{i}.html"
        response = requests.get(url)
        if response.ok: #Vérification de la connexion à la page
            soup = BeautifulSoup(response.text, 'html.parser')
            all_book_on_page = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3") #Récupération des livres présents sur la page
            
            for book in all_book_on_page:
                a = book.find('a')
                list_all_url.append("https://books.toscrape.com/catalogue/category/books/historical-fiction_4/" + a['href'])
        
    print("Nombre d'URL récupéré: ", len(list_all_url))
    return list_all_url

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
    

number_of_page = total_of_page()
all_books_category = collect_books_name(number_of_page)

for book in all_books_category:
    print(book)
