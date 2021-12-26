from flask_restx import Namespace, fields, Resource

from src import db
from src.db_models import Library

api = Namespace('Libraries')

LibraryPayloadModel = api.model("LibraryPayloadModel", {
    'name': fields.String(required=True, min_length=1, max_length=100),
    'city': fields.String(required=True, min_length=1, max_length=150),
    'state': fields.String(required=True, min_length=1, max_length=150),
    'postal_code': fields.String(required=True, min_length=1, max_length=150),
})

LibraryBaseResponseModel = api.model("LibraryBaseResponseModel", {
    'id': fields.String(required=True, min_length=1, max_length=100),
    'name': fields.String(required=True, min_length=1, max_length=100),
    'city': fields.String(required=True, min_length=1, max_length=150),
    'state': fields.String(required=True, min_length=1, max_length=150),
    'postal_code': fields.String(required=True, min_length=1, max_length=150),
})

LibraryResponseModel = api.model("LibraryResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.Nested(LibraryBaseResponseModel, skip_none=True)
})

LibraryListResponseModel = api.model("LibraryListResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.List(fields.Nested(LibraryBaseResponseModel, skip_none=True), skip_none=True)
})


@api.route("")
class LibrariesResource(Resource):

    @api.response(200, "Library Created Successfully", LibraryResponseModel)
    @api.expect(LibraryPayloadModel, validate=True)
    @api.marshal_with(LibraryResponseModel, skip_none=True)
    def post(self):
        """ Create New Library """
        payload = api.payload
        book = Library(payload)
        db.session.add(book)
        db.session.commit()
        payload['id'] = book.id
        return {'code': '200', 'message': 'Library Created Successfully', 'data': payload}

    @api.response(200, "Library List Returned", LibraryListResponseModel)
    @api.marshal_with(LibraryListResponseModel)
    def get(self):
        """ Get All Libraries """
        books = db.session.query(Library.id, Library.name, Library.city, Library.state, Library.postal_code).order_by(Library.name).all()

        return {'code': '200', 'message': 'Library List Returned', 'data': books}


@api.route("/<string:library_id>")
class LibraryByIdResource(Resource):
    pass
