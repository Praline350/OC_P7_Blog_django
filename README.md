# Blog Litéraire LitRevu

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Django](https://img.shields.io/badge/Django-3.2-green)
![Python](https://img.shields.io/badge/Python-3.8-blue)


Projet Openclassroom.
Cette application web/blog permettant de publier et demander des critiques de livres ou d’articles, les utilsateurs peuvent gérer leurs profils, gérer leurs tickets et reviews et interragir entre eux via les follows ou les reviews sur le feed.


## Table des Matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)


## Installation

### Prérequis

- Python 3.8+
- Django 3.2+
- Git

### Étapes

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/tonnom/repository.git

2. Accedez au repository :
    ```bash
    cd repository

3. Créer et activer l'environnement virtuel
    ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows : env\Scripts\activate

4. Installez les dépendances :
    ```bash 
    pip install -r requirements.txt

5. Appliquez les migrations :
    ```bash
    python manage.py migrate
6. Lancez le serveur de développement :
    ```bash
    python manage.py runserver

7. Ouvrez votre navigateur et accédez à http://127.0.0.1:8000/


## Utilisation

#### Fonctionnalitées
````
1. Enregistrez-vous ou connectez-vous pour accéder à toutes les fonctionnalités.
2. Utilisez le formulaire de publication pour demander des critiques de livres ou d’articles.
3. Repondez aux tickets avec une critiques via les tickets diretements
4. Demandez des critiques en soumettant un ticket avec les détails du livre ou de l’article.
5. Personnalisez votre profil en téléchargeant une photo de profil et en utilisant le Cropper JS intégré.
6. Suivez d'autre utilisateur pour accedez à leurs tickets.
7. Bloquer certains utilisateurs pour qu'il n'apparaissent plus.
8. Recherchez des utilisateurs avec la barre de recherche
9. Consultez les follows et posts d'autre utilisateurs sur leurs profil
````

#### Fonctionnalitées avancées
````
- L'API Google Books pour remplir automatiquement les informations des tickets en saisissant simplement le titre du livre.
- Affichez les critiques et les tickets dans deux flux différents : un flux général et un flux des suivis.
````


## Contribuer

Les contributions sont les bienvenues ! Veuillez suivre les étapes ci-dessous pour contribuer :
````
1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez votre branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request
````
