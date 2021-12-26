from flask_restx import Namespace, fields, Resource

from src import db, BusinessRuleConflictError
from src.db_models import User

api = Namespace('Users')

UserAccountPayload = api.model("UserAccountPayload", {
    'name': fields.String(required=True, min_length=1, max_length=50),
    "email": fields.String(required=True, min_length=1, max_length=100),
})
UserAccountBaseResponse = api.model("UserAccountBaseResponse", {
    'id': fields.String(required=True, min_length=1, max_length=50),
    'name': fields.String(required=True, min_length=1, max_length=50),
    "email": fields.String(required=True, min_length=1, max_length=100),
})
UserAccountResponse = api.model("UserAccountResponse", {
    "status": fields.String(),
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.Nested(UserAccountBaseResponse, required=True, skip_none=True)
})

UserAccountListResponse = api.model("UserProfileListResponse", {
    "status": fields.String(),
    "code": fields.String(),
    "message": fields.String(),
    "data": fields.List(fields.Nested(UserAccountBaseResponse, required=True, skip_none=True), skip_none=True)
})


@api.route("")
class UsersResource(Resource):

    @api.response(404, 'User Not Found')
    @api.response(200, 'User List Returned', UserAccountListResponse)
    @api.marshal_with(UserAccountListResponse, skip_none=True)
    def get(self):
        """ Get User List"""
        try:
            users = db.session.query(User.id, User.name, User.email).all()
            response = {
                "status": "Success",
                "code": "200",
                "message": 'User List Returned',
                "data": users
            }
            return response

        finally:
            pass

    @api.response(404, 'User Not Found')
    @api.response(200, 'User Account Created', UserAccountResponse)
    @api.expect(UserAccountPayload, validate=True)
    @api.marshal_with(UserAccountResponse, skip_none=True)
    def post(self):
        """Create New User"""
        try:
            payload = api.payload

            user = db.session.query(User).filter_by(email=payload['email']).first()
            if user:
                raise BusinessRuleConflictError('Email Already Exist')
            user = User(payload)
            db.session.add(user)
            db.session.commit()
            payload['id'] = user.id
            response = {
                "status": "Success",
                "code": "200",
                "message": 'User Account Created',
                "data": payload
            }
            return response

        finally:
            pass
