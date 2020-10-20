from werkzeug.exceptions import HTTPException

"""Database Exceptions"""


class NotFound(HTTPException):
    def __init__(self, obj):
        self.description = f"{type(obj).__name__} object not found."
        self.code = 404
        self.response = {'message': self.description}, self.code


class AlreadyExists(HTTPException):
    def __init__(self, obj):
        self.description = f"{type(obj).__name__} already exists. {obj.unique_fields()} must be unique."
        self.code = 409
        self.response = {'message': self.description}, self.code


class OtherException(HTTPException):
    def __init__(self, obj):
        self.description = f"Unexpected errors occurred on {type(obj).__name__}."
        self.code = 500
        self.response = {'message': self.description}, self.code


class ViolateFKConstraint(HTTPException):
    def __init__(self, obj):
        self.description = f"Violate Referential constraint while manipulating {type(obj).__name__}."
        self.code = 400
        self.response = {'message': self.description}, self.code


class MultipleRecordsFound(HTTPException):
    def __init__(self, obj):
        self.description = f"Multiple records found for {type(obj).__name__}."
        self.code = 400
        self.response = {'message': self.description}, self.code


"""Business Logic Exceptions"""


class LackRequiredData(HTTPException):
    """Lack required data"""
    code = 400
    description = "Lack required data."

    def __init__(self, msg):
        self.description = f"Lack required data: '{msg}'."
        self.response = {'message': self.description}, self.code
