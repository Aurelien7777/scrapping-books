import requests
from bs4 import BeautifulSoup
import time

list_all_url = []

for i in range(2):
    i += 1
    print(f"Page numéro {i} de la catégorie")
    url = f"https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-{i}.html"
    response = requests.get(url)
    if response.ok:
        print(response)
        soup = BeautifulSoup(response.text, 'html.parser')

        all_book_on_page = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        compteur = 0
        for book in all_book_on_page:
            compteur += 1
            print(f"Livre {compteur} analysé de la page: {i}")
            a = book.find('a')
            list_all_url.append("https://books.toscrape.com/catalogue/category/books/historical-fiction_4/" + a['href'])
            print(f"Ajout dans la liste du livre {compteur} effectué")     
print(len(list_all_url))






def collect_books_name(url_page):
    pass

