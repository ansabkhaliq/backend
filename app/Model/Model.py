import json
from decimal import Decimal
from pymysql import IntegrityError
from app.Resource.DatabaseBase import DatabaseBase as DB

class Model:
    """
    A base class for the database models. Responsible for
    deserializing JSON objects into the specific model classes,
    and serializing the model objects back into JSON strings
    """

    def __init__(self, obj):
        """
        Super constructor deserializes the input dictionary (i.e. JSON object)
        into the specific model subclass

        Params:
            obj: a JSON object (dictionary)
        """
        self.__dict__.update(json.loads(json.dumps(obj)))
        for key in self.__dict__:
            if type(self.__dict__[key]) == Decimal:
                self.__dict__[key] = float(self.__dict__[key])

    def json(self):
        """
        Serializes the subclass model object into a JSON string
        """
        return json.dumps(self.__dict__)
