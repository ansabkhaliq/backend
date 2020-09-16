from . import Model

class Organization(Model):
    def __init__(self, json):
        self.orgId = None
        self.apiOrgKey = None
        self.apiOrgPassword = None
        super().__init__(json)
