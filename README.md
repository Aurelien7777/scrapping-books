# Books Online — Système de surveillance des prix (version bêta)

## 1. Contexte et objectif du projet
Ce projet a été développé dans le cadre du parcours **OpenClassrooms — Utilisez les bases de Python pour l'analyse de marché**.

### Mission
Ce projet met en place un **scraper Python** pour le site [Books to Scrape](https://books.toscrape.com/), permettant d’extraire automatiquement les données suivantes :

- URL de la page produit
- UPC (Universal Product Code)
- Titre du livre
- Prix TTC et HT
- Disponibilité
- Description
- Catégorie
- Note (Review Rating)
- URL de l’image

Le script :
- **Collecte** les données pour toutes les catégories du site
- **Enregistre** un fichier CSV par catégorie dans le dossier `COLLECT_DATA`
- **Télécharge** toutes les images dans un dossier spécifique par catégorie


## 2. Instructions d’installation

### Prérequis
- **Python** ≥ 3.8
- Connexion Internet
- Environnement virtuel recommandé (venv ou conda)

### Installation des dépendances
1. Cloner le projet :

git clone https://github.com/Aurelien7777/scrapping-books.git


2. Créer et activer un environnement virtuel :

python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows


3. Installer les dépendances

pip install -r requirements.txt


## 3. Comment exécuter le script
Lancer le script principal depuis la racine du projet :
python scrapping_total_final.py

Le script :

Crée un dossier COLLECT_DATA contenant un fichier CSV par catégorie.

Crée un dossier d’images par catégorie (ex. IMAGE_CATEGORY_travel).

Télécharge et enregistre toutes les données et images localement.


## 4. Explication des fichiers importants

-  scrapping_total_final.py	= Script principal contenant le code de scraping
- requirements.txt	= Liste des dépendances nécessaires au projet
- .gitignore	=  Fichier pour exclure les fichiers/dossiers non suivis (CSV, images, venv, etc.)
- COLLECT_DATA/ (généré)	=  Contient les CSV par catégorie
- IMAGE_CATEGORY_<nom_catégorie>/ (généré)	=  Contient les images par catégorie
- README.md	=  Documentation du projet


## 5. Contact / Ressources pour aide

Auteur : Amorin Aurélien
E-mail : Aurelien.amorin@gmail.com

Ressources utilisées :

- Documentation Python : https://docs.python.org/fr/3/

- Requests : https://requests.readthedocs.io/

- BeautifulSoup4 : https://www.crummy.com/software/BeautifulSoup/bs4/doc/

- Books to Scrape : https://books.toscrape.com/






