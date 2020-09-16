from . import Model

class User(Model):
    def __init__(self, json):
        self.UUID = None  # using UUID Or auto increment?
        self.org_id = None
        self.userName = None
        self.password = None
        super().__init__(json)
