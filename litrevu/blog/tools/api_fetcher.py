import os
import requests
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


class APIFetcher:
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
            return data.get('items', [])
        return None

def search_books_api(request):
    query = request.GET.get('query', '')
    fetcher = APIFetcher()
    books = fetcher.get_books(query)
    book_list = []
    for book in books:
        volume_info = book.get('volumeInfo', {})
        title = volume_info.get('title', 'Titre inconnu')
        authors = ', '.join(volume_info.get('authors', ['Auteur inconnu']))
        image = volume_info.get('imageLinks', {}).get('thumbnail', '')
        book_list.append({'title': title, 'authors': authors, 'image': image})
    return JsonResponse({'books': book_list})
        


query = 'Harry Potter'
fetcher = APIFecther()
books = fetcher.get_books(query)

for title in titles:
    print(title)
