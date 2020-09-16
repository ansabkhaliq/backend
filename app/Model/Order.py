from . import Model

class Order(Model):
    def __init__(self, json):
        self.id = None
        self.keyPurchaseOrderId = None
        self.organizationId = None
        self.keySupplierAccountID = None
        self.supplierOrgId = None
        self.createdDate = None
        self.instruction = None
        self.deliveryOrgName = None
        self.deliveryContact = None
        self.deliveryEmail = None
        self.deliveryAddress1 = None
        self.deliveryAddress2 = None
        self.deliveryAddress3 = None
        self.deliveryRegionName = None
        self.deliveryCountryName = None
        self.deliveryPostcode = None
        self.billingContact = None
        self.billingOrgName = None
        self.billingEmail = None
        self.billingAddress1 = None
        self.billingAddress2 = None
        self.billingAddress3 = None
        self.billingRegionName = None
        self.billingCountryName = None
        self.billingPostcode = None
        self.isDropship = None
        self.orderDetailList = None  # store order detail object
        self.bill_status = None
        self.session_id = None
        super().__init__(json)
