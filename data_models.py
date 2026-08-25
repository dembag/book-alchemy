from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    death_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return (f"Author(id = {self.id}, name = {self.name}, birth_date = {self.birth_date},"
                f" death_date = {self.death_date})")

    def __str__(self):
        return (f"Author(id = {self.id}, name = {self.name}, birth_date = {self.birth_date},"
                f" death_date = {self.death_date})")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(300), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    author = db.relationship("Author", backref="books")

    def __repr__(self):
        return (f"Book(id = {self.id}, isbn = {self.isbn}, title = {self.title},"
                f" publication_year = {self.publication_year}, author_id = {self.author_id})")

    def __str__(self):
        return (f"Book(id = {self.id}, isbn = {self.isbn}, title = {self.title},"
                f" publication_year = {self.publication_year}, author_id = {self.author_id})")
