from werkzeug.exceptions import HTTPException


class LackRequiredData(HTTPException):
    """Lack required data"""
    code = 400
    description = "Lack required data."

    def __init__(self, msg):
        self.description = f"Lack required data: '{msg}'."
        self.response = {'message': self.description}, self.code


# exceptions = {LackRequiredData}
