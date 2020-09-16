class Product:
    def __init__(self):
        self.id = 0
        self.barcode = None
        self.barcodeInner = None
        self.description1 = None
        self.height = 0
        self.internalID = None
        self.isKitted = None
        self.isPriceTaxInclusive = None
        self.keyProductID = None
        self.keySellUnitID = None
        self.keyTaxCodeID = None
        self.kitProductsSetPrice = None
        self.name = None
        self.productCode = None
        self.productSearchCode = None
        # todo: I recommend storing a list in product the list of primary key of sellUnits it is a many to many relation
        self.sellUnits = None
        self.stockLowQuantity = 0
        self.stockQuantity = 0
        self.width = 0
        self.categoryList = None  # store category object
        self.priceList = None  # store price object
        self.sellUnitsIdList = None
        self.description = None
