import time

import requests
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))
GOOGLE_BOOKS_API = os.getenv("GOOGLE_BOOKS_API")

def fetch_cover_from_api(isbn):
    """ Gets book information from Google Books API by author and language."""
    url = "https://www.googleapis.com/books/v1/volumes"

    query = f"isbn:{isbn}"

    params = {
        "q": query,
        "key": GOOGLE_BOOKS_API
    }


    # Query API
    response = None
    max_retries = 3
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            break
        except requests.exceptions.ConnectionError:
            print("Could not connect to Google Books API. Check your internet connection.")
            if attempt < max_retries:
                time.sleep(2)
                continue
            return None
        except requests.exceptions.Timeout:
            print("Request timed out. Retrying..." if attempt < max_retries else "Request timed out. Please try again.")
            if attempt < max_retries:
                time.sleep(2)
                continue
            return None
        except requests.exceptions.HTTPError as e:
            if response is not None and response.status_code == 503 and attempt < max_retries:
                print(f"503 from API, retrying ({attempt +1}/{max_retries})...")
                time.sleep(2)
                continue
            print(f"API returned an error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    book_data = response.json()

    if "items" not in book_data or not book_data["items"]:
        return None

    volume_info = book_data["items"][0].get("volumeInfo", {})
    thumbnail = volume_info.get("imageLinks", {}).get("thumbnail")

    return thumbnail



