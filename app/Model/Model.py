import json

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


    def json(self):
        """
        Deserializes the subclass model object into a JSON string
        """
        return json.dumps(self.__dict__)