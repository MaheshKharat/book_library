from uuid import uuid4
from src.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.String(), primary_key=True, index=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True, index=True)
    token = db.Column(db.String())

    book_activities = db.relationship("LibraryActivity", cascade="save-update, delete")

    def __init__(self, payload):
        self.id = str(uuid4())
        self.name = payload['name']
        self.email = payload['email']


class LibraryStaff(User):
    pass


class Library(db.Model):
    __tablename__ = 'libraries'
    id = db.Column('id', db.String(), primary_key=True, index=True)
    name = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    postal_code = db.Column(db.String())

    records = db.relationship("LibraryBookRecord", cascade="save-update, delete")

    def __init__(self, payload):
        self.id = str(uuid4())
        self.name = payload['name']
        self.city = payload['city']
        self.state = payload['state']
        self.postal_code = payload['postal_code']


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column('id', db.String(), primary_key=True, index=True)
    title = db.Column(db.String())
    author_name = db.Column(db.String())
    isbn_number = db.Column(db.String())
    generation = db.Column(db.String())
    description = db.Column(db.String())

    records = db.relationship("LibraryBookRecord", cascade="save-update, delete")

    def __init__(self, payload):
        self.id = str(uuid4())
        self.title = payload['title']
        self.author_name = payload['author_name']
        self.isbn_number = payload['isbn_number']
        self.generation = payload['generation']
        self.description = payload['description']


class LibraryBookRecord(db.Model):
    __tablename__ = 'library_book_records'
    id = db.Column('id', db.String(), primary_key=True, index=True)
    book_id = db.Column(db.String(), db.ForeignKey('books.id'))
    library_id = db.Column(db.String(), db.ForeignKey('libraries.id'))
    last_activity_library_id = db.Column(db.String())

    book_activities = db.relationship("LibraryActivity", cascade="save-update, delete")

    def __init__(self, payload):
        self.id = str(uuid4())
        self.book_id = payload['book_id']
        self.library_id = payload['library_id']

    def update_last_activity(self, last_activity_library_id):
        self.last_activity_library_id = last_activity_library_id


class LibraryActivity(db.Model):
    __tablename__ = 'library_activities'
    id = db.Column('id', db.String(), primary_key=True, index=True)
    activity_type = db.Column(db.String())
    library_book_id = db.Column(db.String(), db.ForeignKey('library_book_records.id'))
    user_id = db.Column(db.String(), db.ForeignKey('users.id'))
    checked_out_at = db.Column(db.DateTime())
    checked_in_at = db.Column(db.DateTime())

    def __init__(self, payload):
        self.id = str(uuid4())
        self.activity_type = payload['activity_type']
        self.library_book_id = payload.get('library_book_id')
        self.user_id = payload['user_id']
        self.checked_out_at = payload.get('checked_out_at')
        self.checked_in_at = payload.get('checked_in_at')

