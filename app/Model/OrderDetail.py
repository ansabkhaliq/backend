from app.Model.Model import Model

class OrderDetail(Model):
    def __init__(self, json):
        self.id = None  # autoincrement pk
        self.lineType = None  # don't understand all the type is PRODUCT
        self.keyProductID = None  # Unique key in product
        self.productName = None
        self.quantity = None
        self.unitPrice = None
        self.totalPrice = None  # instead priceTotalTax, I use this as totalPrice
        self.priceTotalIncTax = None  # there is no where to record the tax can delete these
        self.priceTotalExTax = None
        self.productCode = None  # same with product code in product
        self.productId = None  # our own product_id
        self.orderId=None #store the relationship of order
        super().__init__(json)
