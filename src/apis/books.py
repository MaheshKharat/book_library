from flask_restx import Namespace, fields, Resource

from src import db
from src.db_models import Book

api = Namespace('Books')

BookPayloadModel = api.model("BookPayloadModel", {
    'title': fields.String(required=True, min_length=1, max_length=100),
    'author_name': fields.String(required=True, min_length=1, max_length=150),
    'isbn_number': fields.String(required=True, min_length=1, max_length=150),
    'generation': fields.String(required=True, min_length=1, max_length=150),
    'description': fields.String(required=True, min_length=1, max_length=150),
})

BookBaseResponseModel = api.model("BookBaseResponseModel", {
    'id': fields.String(required=True, min_length=1, max_length=100),
    'title': fields.String(required=True, min_length=1, max_length=100),
    'author_name': fields.String(required=True, min_length=1, max_length=150),
    'isbn_number': fields.String(required=True, min_length=1, max_length=150),
    'generation': fields.String(required=True, min_length=1, max_length=150),
    'description': fields.String(required=True, min_length=1, max_length=150),
})

BookResponseModel = api.model("BookResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.Nested(BookBaseResponseModel, skip_none=True)
})

BookListResponseModel = api.model("BookListResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.List(fields.Nested(BookBaseResponseModel, skip_none=True), skip_none=True)
})


@api.route("")
class BooksResource(Resource):

    @api.response(200, "Book Created Successfully", BookResponseModel)
    @api.expect(BookPayloadModel, validate=True)
    @api.marshal_with(BookResponseModel, skip_none=True)
    def post(self):
        """ Create New Book """
        payload = api.payload
        book = Book(payload)
        db.session.add(book)
        db.session.commit()
        payload['id'] = book.id
        return {'code': '200', 'message': 'Book Created Successfully', 'data': payload}

    @api.response(200, "Book List Returned", BookListResponseModel)
    @api.marshal_with(BookListResponseModel)
    def get(self):
        """ Get All Books """
        books = db.session.query(Book.id, Book.title, Book.author_name, Book.description, Book.generation, Book.isbn_number).order_by(Book.title).all()

        return {'code': '200', 'message': 'Book List Returned', 'data': books}


@api.route("/<string:book_id>")
class BookByIdResource(Resource):
    pass
