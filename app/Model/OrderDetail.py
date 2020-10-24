from app.Model.Model import Model


class OrderDetail(Model):
    def __init__(self, json):
        self.id = None  # autoincrement pk
        self.lineType = None
        self.keyProductID = None  # Unique key in product
        self.productName = None
        self.quantity = None
        self.unitPrice = None   # Is null for now since SQUIZZ is not returning unitPrice in JSON, however, unit prices are found in totalPriceExTax field in DB
        self.totalPrice = None  # instead priceTotalTax, I use this as totalPrice
        self.priceTotalIncTax = None  # there is no where to record the tax can delete these
        self.priceTotalExTax = None
        self.productCode = None  # same with product code in product
        self.productId = None  # our own product_id
        self.orderId = None  # store the relationship of order
        super().__init__(json)

    @staticmethod
    def table_name():
        return 'orderdetails'

    @staticmethod
    def fields_mapping():
        return {
            'id': 'id',
            'keyProductID': 'keyProductId',
            'keyProductId': 'keyProductID',
            'productName': 'productName',
            'quantity': 'quantity',
            'unitPrice': 'unitPrice',
            'totalPrice': 'totalPrice',
            'priceTotalIncTax': 'priceTotalIncTax',
            'priceTotalExTax': 'priceTotalExTax',
            'productCode': 'productCode',
            'orderId': 'orderId',
            'productId': 'productId'
        }
