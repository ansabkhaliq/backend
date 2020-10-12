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

    @staticmethod
    def get_table_name():
        return ''

    def create(self):
        """
        Save current obj as an new instance into the database
        Notice: The Model attributes and table name must be same as those in DB
        Must overwrite the function get_table_name
        """
        db = DB()
        table = self.get_table_name()
        fields = ','.join(self.__dict__.keys())
        values = list(self.__dict__.values())
        place_holders = ('%s,' * len(values))[:-1]
        query = f"INSERT into {table} ({fields}) VALUES ({place_holders})"
        db.run(query, values, True)

    def update(self):
        """
        Save current obj into database according to the id
        Notice: The Model attributes and table name must be same as those in DB
        Must overwrite the function get_table_name
        """
        db = DB()
        table = self.get_table_name()
        field_set = set(self.__dict__.keys())
        field_set.remove('id')
        values = [self.__dict__[field] for field in field_set]
        sets = ','.join([f'{field}=%s' for field in field_set])
        query = f"UPDATE {table} SET {sets} WHERE id={self.id}"
        db.run(query, values, True)
