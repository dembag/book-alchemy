import os
from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

import API_manager
from data_models import db, Author, Book


app = Flask(__name__)

# Connect to database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

# Create tables (run once)
# with app.app_context():
#     db.drop_all()
#     db.create_all()


@app.route("/", methods=["GET"])
def home():
    """
    Displays the books in the database.
    Links to add_author and add_book.
    """
    sort_by = request.args.get("sort_by", "title")
    success = request.args.get("success")

    if sort_by == "author":
        sorted_books = Book.query.join(Book.author).order_by(Author.name).all()
    else:
        sorted_books = Book.query.order_by(Book.title).all()

    return render_template("home.html", books=sorted_books, sort_by=sort_by,
                            success=success)


@app.route("/search", methods=["GET"])
def search():
    """ The user can search books for keywords."""
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("search.html", error=f"No records match that search.",
                                books=[])

    search_term = f"%{query}%"

    books = (
        Book.query.join(Book.author)
        .filter(
            or_(
                Book.title.ilike(search_term),
                Author.name.ilike(search_term)
            )
        )
        .all()
    )

    if not books:
        return render_template("search.html", error=f"No records match '{query}'.",
                                books=[])

    return render_template("search.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Displays add_author.html.
    GET  - Displays form to enter Author name, birth and death dates.
    POST - Adds the form information to the database.
         - Displays a success message.
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birth_date_str = request.form.get("birthdate")
        death_date_str = request.form.get("date_of_death")

        if not name:
            return render_template("add_author.html",
                                   error="Author name cannot be empty.")
        try:
            birth_date = (
                datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                if birth_date_str else None
            )
            death_date = (
                datetime.strptime(death_date_str, "%Y-%m-%d").date()
                if death_date_str else None
            )
        except ValueError:
            return render_template("add_author.html", error="Invalid date format.")

        if birth_date and death_date and death_date < birth_date:
            return render_template("add_author.html",
                                   error="Date of death cannot be before birth date.")

        # Create instance of author
        new_author = Author(
            name=name,
            birth_date=birth_date,
            death_date=death_date
        )

        # Add to database
        try:
            db.session.add(new_author)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("add_author.html", error=f"Failed to add author: {e}")

        return render_template("add_author.html", success=f"{name} added to authors list.")

    # for GET
    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Displays add_book.html.
    GET  - Displays form to enter book information
    POST - Adds the information to the table
    """
    authors = Author.query.all()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author_id = request.form.get("author_id", "").strip()
        isbn = request.form.get("isbn", "").strip()
        year_str = request.form.get("year", "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if not isbn:
            errors.append("ISBN is required.")
        if not author_id:
            errors.append("Please select an author.")
        if year_str and not year_str.isdigit():
            errors.append("Year must be a number.")

        if errors:
            return render_template("add_book.html", error=" ".join(errors), authors=authors)

        year = int(year_str) if year_str else None

        cover_url = API_manager.fetch_cover_from_api(isbn)

        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=year,
            cover_url=cover_url,
            author_id=author_id
        )
        try:
            db.session.add(new_book)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("add_book.html",
                                   error="That ISBN already exists.",
                                   authors=authors)
        except Exception as e:
            db.session.rollback()
            return render_template("add_book.html",
                                   error=f"Failed to add book: {e}",
                                   authors=authors)

        return render_template("add_book.html",
                               success=f"{title} added to books list.",
                               authors=authors)

    return render_template("add_book.html", authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author
    author_name = author.name
    deleted_title = book.title
    db.session.delete(book)
    db.session.commit()

    if not author.books:
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for("home",
                                success=f"{deleted_title} successfully deleted.\n"
                                        f"{author_name} had no books left in the database "
                                        f"and was also deleted."))

    return redirect(url_for("home", success=f"{deleted_title} successfully deleted."))



if __name__ == "__main__":

    app.run(debug=True)
