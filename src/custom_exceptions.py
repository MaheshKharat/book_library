

class BaseError(Exception):
    """Base Error Class"""

    def __init__(self, message='', errors=None):
        super().__init__()
        self.code = 400
        self.message = message
        self.status = "BAD_REQUEST"
        if not errors:
            errors = {}
        self.errors = errors

    def to_dict(self):
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "errors": self.errors
        }


class NotFoundError(BaseError):
    def __init__(self, message, errors=None):
        super().__init__(message, errors)
        self.code = 404
        self.status = "NOT_FOUND"


class NotAuthorizedError(BaseError):
    def __init__(self, message, errors=None):
        super().__init__(message, errors)
        self.code = 401
        self.status = "NOT_AUTHORIZED"


class BusinessRuleConflictError(BaseError):
    def __init__(self, message, errors=None):
        super().__init__(message, errors)
        self.code = 409
        self.status = "BUSINESS_RULE_FAILURE"

