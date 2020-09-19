from app.Model.Model import Model


class Product(Model):
    def __init__(self, json):
        self.id = 0
        self.barcode = None
        self.barcodeInner = None
        self.description1 = None
        self.description2 = None
        self.description3 = None
        self.description4 = None
        self.height = 0
        self.internalID = None
        self.brand = None
        self.depth = 0
        self.weight = 0
        self.volume = 0
        self.isKitted = None
        self.isPriceTaxInclusive = None
        self.productCondition = None
        self.keyProductID = None
        self.keySellUnitID = None
        self.keyTaxcodeID = None
        self.kitProductsSetPrice = None
        self.name = None
        self.productCode = None
        self.productSearchCode = None
        self.averageCost = None
        self.drop = None
        self.packQuantity = None
        self.sellUnits = None
        self.stockLowQuantity = 0
        self.stockQuantity = 0
        self.width = 0
        self.categoryList = None  # store category object
        self.priceList = None  # store price object
        self.sellUnitsIdList = None  # sell the SellUnitIds (new table)
        self.imageList = None  # List to store the images associated with the product
        super().__init__(json)
