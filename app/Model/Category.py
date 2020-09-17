from app.Model.Model import Model


class Category(Model):
    def __init__(self, json):
        self.id = 0
        self.categoryCode = None
        self.description1 = None
        self.description2 = None
        self.description3 = None
        self.description4 = None
        self.internalID = None
        self.keyCategoryID = None
        self.keyCategoryParentID = None
        self.metaDescription = None
        self.metaKeywords = None
        self.name = None
        self.ordering = 0
        self.productList = None  # store product object
        super().__init__(json)
