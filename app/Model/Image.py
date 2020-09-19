from app.Model.Model import Model

class Image(Model):
    def __init__(self, json):
        self.id = 0
        self.fileName = None
        self.smallImageLocation = None
        self.mediumImageLocation = 0
        self.largeImageLocation = None
        self.threeDModelLocation = None
        self.is3DModelType = 'N'
        # Foreign Key for product.
        self.productId = None
        super().__init__(json)
