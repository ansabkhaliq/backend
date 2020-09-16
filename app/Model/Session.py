from app.Model.Model import Model

class Session(Model):
    def __init__(self, json):
        self.id = None
        self.sessionKey = None
        self.orgId = None
        super().__init__(json)

