from app.Model.Model import Model

class Price(Model):
    def __init__(self, json):
        # primary key
        self.id = 0
        # foreignkey--connect to product
        self.keyProductId = None
        # foreignkey -- connect to unit
        self.keyUnitId = None
        # price
        self.price = 0
        # I don't know the meaning since it occurs every where
        self.referenceId = None
        self.referenceType = None
        self.productId = None
        super().__init__(json)
