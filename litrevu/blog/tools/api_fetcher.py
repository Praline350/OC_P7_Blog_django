import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


class APIFecther:
    def __init__(self):
        self.url = 'https://www.googleapis.com/books/v1/volumes'
        self.key = os.getenv('API_KEY')

    def get_books(self, query):
        url = 'https://www.googleapis.com/books/v1/volumes'
        params = {
            'key': self.key,  # Remplace cette valeur par ta propre clé d'API
            'q': query,
            'maxResults': 10
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                # Récupère le titre du premier livre trouvé
                return data.get('items', [])   
        return None

    def get_titles(self, books):
        titles = []
        for book in books:
            volume_info = book.get('volumeInfo', {})
            title = volume_info.get('title', 'Titre inconnu')
            titles.append(title)
        return titles
        


query = 'Harry Potter'
fetcher = APIFecther()
books = fetcher.get_books(query)
titles = fetcher.get_titles(books)
for title in titles:
    print(title)
