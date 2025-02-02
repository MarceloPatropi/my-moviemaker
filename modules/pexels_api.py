import requests
from dotenv import load_dotenv
import os

class PexelsAPI:
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("PEXELS_API_KEY")
        self.base_url_video = "https://api.pexels.com/videos/"
        self.base_url_photo = "https://api.pexels.com/v1/"
        self.headers = {
            "Authorization": self.api_key
        }

    def search_photos(self, query, per_page=15, page=1):
        url = f"{self.base_url_photo}search"
        params = {
            "query": query,
            "per_page": per_page,
            "page": page,
            "orientation": "landscape",
            "size": "large",
            "locale": "pt-BR"
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def search_videos(self, query, per_page=15, page=1):
        url = f"{self.base_url_video}search"
        params = {
            "query": query,
            "per_page": per_page,
            "page": page,
            "orientation": "landscape",
            "size": "large",
            "locale": "pt-BR"
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

# Exemplo de uso
if __name__ == "__main__":
    pexels = PexelsAPI()
    
    # Buscar fotos
    photos = pexels.search_photos("natureza")
    print("Fotos encontradas:", photos)
    
    # Buscar vídeos
    videos = pexels.search_videos("natureza")
    print("Vídeos encontrados:", videos)
