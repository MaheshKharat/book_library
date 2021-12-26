import datetime

from flask_restx import Namespace, fields, Resource
from flask_restx.reqparse import RequestParser

from src.db import db
from src.custom_exceptions import NotFoundError, BusinessRuleConflictError
from src.constants import ActivityTypes
from src.db_models import LibraryBookRecord, LibraryActivity, Book, Library, User

api = Namespace('Library Book Record')

LibraryBookRecordPayloadModel = api.model("LibraryBookRecordPayloadModel", {
    'book_id': fields.String(required=True, min_length=1, max_length=100),
    'library_id': fields.String(required=True, min_length=1, max_length=100),
})

LibraryBookRecordBaseResponseModel = api.model("LibraryBookRecordBaseResponseModel", {
    'id': fields.String(required=True, min_length=1, max_length=100),
    'book_id': fields.String(required=True, min_length=1, max_length=100),
    'library_id': fields.String(required=True, min_length=1, max_length=150),
})

LibraryBookRecordResponseModel = api.model("LibraryBookRecordResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.Nested(LibraryBookRecordBaseResponseModel, skip_none=True)
})

LibraryBookRecordListResponseModel = api.model("LibraryBookRecordListResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.List(fields.Nested(LibraryBookRecordBaseResponseModel, skip_none=True), skip_none=True)
})


@api.route("")
class LibrariesResource(Resource):

    @api.response(200, "LibraryBookRecord Created Successfully", LibraryBookRecordResponseModel)
    @api.expect(LibraryBookRecordPayloadModel, validate=True)
    @api.marshal_with(LibraryBookRecordResponseModel, skip_none=True)
    def post(self):
        """ Create New LibraryBookRecord """
        payload = api.payload
        book_id = payload['book_id']
        lib_id = payload['library_id']
        book = db.session.query(Book.id).filter_by(id=book_id).first()
        lib = db.session.query(Library.id).filter_by(id=lib_id).first()
        if not book:
            raise NotFoundError('Book Not Found')

        if not lib:
            raise NotFoundError('Library Not Found')

        lib_book = db.session.query(LibraryBookRecord.id).filter(LibraryBookRecord.book_id == book_id, LibraryBookRecord.library_id == lib_id).first()
        if lib_book:
            raise BusinessRuleConflictError('Book Entry Already Exist')

        book = LibraryBookRecord(payload)
        db.session.add(book)
        db.session.commit()
        payload['id'] = book.id
        return {'code': '200', 'message': 'LibraryBookRecord Created Successfully', 'data': payload}

    @api.response(200, "LibraryBookRecord List Returned", LibraryBookRecordListResponseModel)
    @api.marshal_with(LibraryBookRecordListResponseModel)
    def get(self):
        """ Get All Library Book Records """
        books = db.session.query(LibraryBookRecord.id, LibraryBookRecord.library_id, LibraryBookRecord.book_id).all()

        return {'code': '200', 'message': 'LibraryBookRecord List Returned', 'data': books}


LibraryBookCheckInOutPayloadModel = api.model("LibraryBookCheckInOutPayloadModel", {
    'user_id': fields.String(required=True, min_length=1, max_length=100),
    'activity_type': fields.String(required=True, min_length=1, max_length=100, enum=[ActivityTypes.BOOK_CHECK_OUT, ActivityTypes.BOOK_CHECK_IN]),
})

LibraryBookCheckInOutBaseResponseModel = api.model("LibraryBookCheckInOutBaseResponseModel", {
    'id': fields.String(required=True, min_length=1, max_length=100),
    'library_book_id': fields.String(required=True, min_length=1, max_length=100),
    'user_id': fields.String(required=True, min_length=1, max_length=100),
    'activity_type': fields.String(required=True, min_length=1, max_length=100, enum=[ActivityTypes.BOOK_CHECK_OUT, ActivityTypes.BOOK_CHECK_IN]),
})

LibraryBookCheckInRecordResponseModel = api.model("LibraryBookCheckInRecordResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.Nested(LibraryBookCheckInOutBaseResponseModel, skip_none=True)
})

LibraryBookCheckInRecordListResponseModel = api.model("LibraryBookCheckInRecordListResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.Nested(LibraryBookCheckInOutBaseResponseModel, skip_none=True)
})


@api.route("/<string:library_book_id>/activities")
class LibraryBookCheckOutByIdResource(Resource):
    @api.response(200, "Success", LibraryBookCheckInRecordResponseModel)
    @api.expect(LibraryBookCheckInOutPayloadModel, validate=True)
    @api.marshal_with(LibraryBookCheckInRecordResponseModel, skip_none=True)
    def post(self, library_book_id):
        """ Book Check IN-Out Activities"""
        payload = api.payload
        lib_book_record = db.session.query(LibraryBookRecord).filter_by(id=library_book_id).first()
        if not lib_book_record:
            raise NotFoundError('Library Book Record Not Found')
        user = db.session.query(User.id).filter_by(id=payload['user_id']).first()
        if not user:
            raise NotFoundError('User Not Found')

        if payload.get('activity_type') == ActivityTypes.BOOK_CHECK_OUT:
            payload['checked_out_at'] = datetime.datetime.now()
        else:
            payload['checked_in_at'] = datetime.datetime.now()

        payload['library_book_id'] = library_book_id
        lib_activity = LibraryActivity(payload)
        db.session.add(lib_activity)
        # Here i updating last activity of book
        lib_book_record.update_last_activity(lib_activity.id)

        db.session.commit()
        payload['id'] = lib_activity.id
        return {'code': '200', 'message': 'Success', 'data': payload}

    @api.response(200, "Library Book Record Activity List Returned", LibraryBookCheckInRecordListResponseModel)
    @api.marshal_with(LibraryBookCheckInRecordListResponseModel)
    def get(self, library_book_id):
        """ Get All Library Book Checked Out Records """
        lib_book = db.session.query(LibraryBookRecord.id).filter_by(id=library_book_id).first()
        if not lib_book:
            raise NotFoundError('Library Book Record Not Found')

        book_activities = db.session.query(LibraryActivity.id, LibraryActivity.user_id, LibraryActivity.library_book_id, LibraryActivity.activity_type, LibraryActivity.checked_in_at, LibraryActivity.checked_out_at)
        book_activities = book_activities.filter(LibraryActivity.library_book_id == library_book_id).all()

        return {'code': '200', 'message': 'Library Book Record Activity List Returned', 'data': book_activities}


LibraryBookBaseResponseModel = api.model("LibraryBookBaseResponseModel", {
    'id': fields.String(required=True, min_length=1, max_length=100),
    'library_book_id': fields.String(required=True, min_length=1, max_length=100),
    'book_id': fields.String(required=True, min_length=1, max_length=100),
    'title': fields.String(required=True, min_length=1, max_length=100),
    'checked_in_at': fields.String(required=True, min_length=1, max_length=100),
    'checked_out_at': fields.String(required=True, min_length=1, max_length=100),
    'activity_type': fields.String(required=True, min_length=1, max_length=100, enum=[ActivityTypes.BOOK_CHECK_OUT, ActivityTypes.BOOK_CHECK_IN]),
})

UserLibraryBookListResponseModel = api.model("UserLibraryBookListResponseModel", {
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.Nested(LibraryBookBaseResponseModel, skip_none=True)
})


@api.route("/find/by_user")
class BookRecordsByUserResource(Resource):
    parser = RequestParser()
    parser.add_argument('user_id', type=str, required=True)

    @api.response(200, "LibraryBookRecord List Returned", UserLibraryBookListResponseModel)
    @api.expect(parser)
    @api.marshal_with(UserLibraryBookListResponseModel)
    def get(self):
        """ Get All Library Book Records By User"""
        args = self.parser.parse_args()
        user_id = args.get('user_id')
        books = db.session.query(LibraryActivity).select_from(LibraryBookRecord).join(Book).filter(LibraryActivity.library_book_id == LibraryBookRecord.id, LibraryBookRecord.book_id == Book.id, LibraryActivity.user_id == user_id)
        books = books.add_columns(Book.id.label('book_id'), Book.title, LibraryBookRecord.library_id, LibraryBookRecord.last_activity_library_id, LibraryActivity.library_book_id, LibraryActivity.activity_type,
                                  LibraryActivity.checked_in_at, LibraryActivity.checked_out_at).all()

        return {'code': '200', 'message': 'LibraryBookRecord List Returned', 'data': books}


@api.route("/find/by_library")
class BookRecordsByLibResource(Resource):
    parser = RequestParser()
    parser.add_argument('library_id', type=str, required=True)

    @api.response(200, "LibraryBookRecord List Returned", UserLibraryBookListResponseModel)
    @api.expect(parser)
    @api.marshal_with(UserLibraryBookListResponseModel)
    def get(self):
        """ Get All Library Book Records By Library"""
        args = self.parser.parse_args()
        library_id = args.get('library_id')
        books = db.session.query(LibraryActivity).select_from(LibraryBookRecord).join(Book).filter(
            LibraryActivity.library_book_id == LibraryBookRecord.id, LibraryBookRecord.book_id == Book.id,
            LibraryBookRecord.library_id == library_id)
        books = books.add_columns(Book.id.label('book_id'), Book.title, LibraryBookRecord.library_id,
                                  LibraryBookRecord.last_activity_library_id, LibraryActivity.library_book_id,
                                  LibraryActivity.activity_type,
                                  LibraryActivity.checked_in_at, LibraryActivity.checked_out_at).all()

        return {'code': '200', 'message': 'LibraryBookRecord List Returned', 'data': books}
