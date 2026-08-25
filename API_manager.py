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
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Could not connect to Google Books API. Check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"API returned an error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    book_data = response.json()

    if "items" not in book_data or not book_data["items"]:
        return None

    volume_info = books_data["items"][0].get("volumeInfo", {})
    thumbnail = volume_info.get("imageLinks", {}).get("thumbnail")

    return thumbnail



