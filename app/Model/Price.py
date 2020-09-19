from app.Model.Model import Model

class Price(Model):
    def __init__(self, json):
        # primary key
        self.id = 0
        self.keyProductID = None
        self.keySellUnitID = None
        self.price = 0
        # Contract Reference ID (not all customers will have it)
        self.referenceID = None
        # Contract Reference Type (not all customers will have it)
        self.referenceType = None
        # foreignkey--connect to product
        self.productId = None
        super().__init__(json)
