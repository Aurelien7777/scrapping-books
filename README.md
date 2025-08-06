# Books Online — Système de surveillance des prix (version bêta)

## 1. Contexte et objectif du projet
Ce projet a été développé dans le cadre du parcours **OpenClassrooms — Utilisez les bases de Python pour l'analyse de marché**.

### Mission
Vous êtes **analyste marketing chez Books Online**, une librairie en ligne spécialisée dans les livres d'occasion.  
Afin de gagner du temps dans la surveillance des prix des concurrents, ce projet met en place un **scraper Python** pour le site [Books to Scrape](https://books.toscrape.com/), permettant d’extraire automatiquement les données suivantes :

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

⚠️ **Les fichiers CSV et images ne doivent pas être versionnés sur GitHub** — ils sont générés à l’exécution.


## 2. Instructions d’installation

### Prérequis
- **Python** ≥ 3.8
- Connexion Internet
- Environnement virtuel recommandé (venv ou conda)

### Installation des dépendances
1. Cloner le projet :

git clone https://github.com/Aurelien7777/scrapping-books.git
cd scrapping-books


2. Créer et activer un environnement virtuel :

python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows


3. Installer les dépendances

pip install -r requirements.txt


## 3. Comment exécuter le script
Lancer le script principal depuis la racine du projet :
python script.py

Le script :

Crée un dossier COLLECT_DATA contenant un fichier CSV par catégorie.

Crée un dossier d’images par catégorie (ex. IMAGE_CATEGORY_travel).

Télécharge et enregistre toutes les données et images localement.


## 4. Explication des fichiers importants

- script.py	= Script principal contenant le code de scraping
- requirements.txt	= Liste des dépendances nécessaires au projet
- .gitignore	=  Fichier pour exclure les fichiers/dossiers non suivis (CSV, images, venv, etc.)
- COLLECT_DATA/ (généré)	=  Contient les CSV par catégorie
- IMAGE_CATEGORY_<nom_catégorie>/ (généré)	=  Contient les images par catégorie
- README.md	=  Documentation du projet

## 5. Contact / Ressources pour aide

Auteur : Amorin Aurélien
E-mail : Aurélien.amorin@gmail.com

Ressources utilisées :

- Documentation Python

- Requests

- BeautifulSoup4

- Books to Scrape






