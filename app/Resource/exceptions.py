from werkzeug.exceptions import HTTPException


class NotFound(HTTPException):
    def __init__(self, obj):
        self.description = f"{type(obj).__name__} object not found."
        self.code = 404
        self.response = {
            'message': self.description
        }, self.code


class AlreadyExists(HTTPException):
    def __init__(self, obj):
        self.description = f"{type(obj).__name__} already exists. {obj.unique_fields()} must be unique."
        self.code = 409


class OtherException(HTTPException):
    def __init__(self, obj):
        self.description = f"Unexpected errors occurred from {type(obj).__name__}."
        self.code = 500
        self.response = {'message': self.description}, self.code


class ViolateFKConstraint(HTTPException):
    def __init__(self, obj):
        self.description = f"Violate Referential constraint while within {type(obj).__name__}."
        self.code = 400
        self.response = {'message': self.description}, self.code


# exceptions = {NotFound, AlreadyExists, OtherException, ViolateFKConstraint}
