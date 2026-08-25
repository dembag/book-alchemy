# Book Alchemy

A Flask web app for managing a personal library. Add authors and books, browse your collection with cover images pulled automatically from the Google Books API, sort by title or author, search by keyword, and delete books (with automatic cleanup of authors who have no books left).

## Features

- **Add authors** with name, birth date, and optional date of death
- **Add books** with title, ISBN, publication year, and linked author
- **Automatic cover art** — fetched from the Google Books API using the book's ISBN
- **Sort** the library by title or author name
- **Search** books by title or author keyword
- **Delete books** — and automatically remove an author if their last book is deleted
- Server-side validation with friendly error messages instead of raw crashes

## Tech Stack

- Python / Flask
- Flask-SQLAlchemy (SQLite)
- Jinja2 templates
- Google Books API (for cover images)

## Requirements

- Python 3.10+
- pip

## Dependencies

```
Flask
Flask-SQLAlchemy
requests
python-dotenv
```

Save these to a `requirements.txt` if you don't already have one.

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/book-alchemy.git
   cd book-alchemy
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a Google Books API key**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project (or select an existing one)
   - Enable the **Books API** under "APIs & Services" → "Library"
   - Go to "Credentials" → "Create Credentials" → "API key"
   - Copy the generated key

4. **Create a `.env` file** in the project root with:
   ```
   GOOGLE_BOOKS_API=your_api_key_here
   ```

5. **Create the database**

   Uncomment these two lines in `app.py`, run the app once, then comment them back out:
   ```python
   # with app.app_context():
   #     db.drop_all()
   #     db.create_all()
   ```

6. **Run the app**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

## Project Structure

```
book-alchemy/
├── app.py              # Flask routes
├── data_models.py      # SQLAlchemy models (Author, Book)
├── API_manager.py      # Google Books API integration
├── data/
│   └── library.sqlite  # SQLite database
├── templates/
│   ├── home.html
│   ├── search.html
│   ├── add_author.html
│   └── add_book.html
├── static/
│   └── style.css
└── .env                # API key (not committed)
```

## Notes

- Books with no matching Google Books cover image will display without an image; this doesn't affect functionality.
- Deleting an author's last remaining book also deletes that author from the database.
