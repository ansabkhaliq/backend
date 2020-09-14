import logging
import requests
import time
from typing import Tuple, Optional


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SquizzGatewayService:
    """
    This class represents a connection, or session, to the SQUIZZ Platform API
    """

    def __init__(self, base_url: str, org_id: str, api_org_key: str, api_org_pw: str, supplier_org_id: str):
        self.base_url = base_url
        self.org_id = org_id
        self.api_org_key = api_org_key
        self.api_org_pw = api_org_pw
        self.supplier_org_id = supplier_org_id
        self.requests = requests.Session()


    # Web Service Endpoint: Create Organisation API Session
    def create_session(self) -> Tuple[str, str]:
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        parameter = {"org_id": self.org_id, "api_org_key": self.api_org_key, "api_org_pw": self.api_org_pw, "create_session": "Y" }
        try:
            data = self.requests.post(self.base_url + "/org/create_session", data = parameter, headers=header).json()    
            if data["result"] == "SUCCESS" and data["result_code"] == "SERVER_SUCCESS":
                logger.info('created a sessoion in squizz')
                return data["session_id"], "LOGIN_SUCCESS"
            else:
                logger.debug('cannot create a sessoion in squizz'+ data["result_code"])
                return None, data["result_code"]
        
        except Exception as e:
            logger.debug("Could not create organisation API session")
            return None, "SERVER_ERROR_UNKNOWN"


    # Web Service Endpoint: Destroy Organisation API Session
    def destory_session(self, session_id: str) -> bool:
        if session_id is None:
            return False
        data = self.requests.get(self.base_url + "/org/destroy_session/" + session_id).json()
        if data["result"] == "SUCCESS":
            logger.info("session destroyed")
            return True
        else:
            logger.debug("Could not destroy organisation API session")
            return False


    # Web Service Endpoint: Validate Organisation API Session
    def validate_session(self, session_id: str) -> bool:
        if session_id is None:
            return False
        data = self.requests.get(self.base_url + "/org/validate_session/" + session_id).json()
        if data["result"] == "SUCCESS":
            if data["session_valid"] == "Y":
                return True
            else:
                return False
        else:
            logger.debug("Could not validate organisation API session")
            return False
    

    # Web Service Endpoint: Product Price Retrieve API
    def get_product_list(self, data_type: int) -> Tuple[bool, Optional[list]]:
        session_id, _ = self.create_session()
        params = {
            "session_id": session_id,
            "supplier_org_id": self.supplier_org_id,
            "data_type_id": data_type
        }
        
        data = self.requests.get("https://api.squizz.com/rest/1/org/retrieve_esd/"+ session_id, params=params).json()
        if data["resultStatus"] == 1:
            return True, data["dataRecords"]
        else:
            return False, None
    

    # Web Service Endpoint: Purchase Submit API
    def submit_purchase(self, jsonValue) -> Tuple[bool, Optional[list]]:
        header = {"Content-Type": "application/json"}
        session_id = jsonValue['sessionKey']
        header = {"Content-Type": "application/json"}

        # I just hardcoded the CustomerAccountCode (we had three, just took one for now), this needs to be generic now. As based on a specific customer we will submit the order. Previously we only had 1 customer so
        # the team was not mentioning the customer. Now we have three.
        purchaseURL = "https://api.squizz.com/rest/1/org/procure_purchase_order_from_supplier/" + session_id +"?supplier_org_id="+self.supplier_org_id \
                      + "&customer_account_code=TESTDEBTOR"

        keyPurchaseOrderID = int(time.time() * 1000000) 
        # Not mandotary details are are hard code for now.
        parameter = {
            "keyPurchaseOrderID": keyPurchaseOrderID,
            "purchaseOrderCode":"test1",
            "purchaseOrderNumber":keyPurchaseOrderID,
            "keySupplierAccountID":"1",
            "supplierAccountCode":"PJSAS",
            "supplierAccountName":"PJ SAS test",
            "deliveryContact":"test",
            "deliveryOrgName":"Acme Industries",
            "deliveryEmail":"js@someemailaddress.comm",
            "deliveryPhone":"+6144433332222",
            "deliveryFax":"+6144433332221",
            "deliveryAddress1":"Unit 5",
            "deliveryAddress2":"22 Bourkie Street",
            "deliveryAddress3":"Melbourne",
            "deliveryPostcode":"3000",
            "deliveryRegionName":"Victoria",
            "deliveryCountryName":"Australia",
            "deliveryCountryCodeISO2":"AU",
            "deliveryCountryCodeISO3":"AUS",
            "billingContact":"John Citizen",
            "billingOrgName":"Acme Industries International",
            "billingEmail":"ms@someemailaddress.comm",
            "billingPhone":"+61445242323423",
            "billingFax":"+61445242323421",
            "billingAddress1":"43",
            "billingAddress2":"Drummond Street",
            "billingAddress3":"Melbourne",
            "billingPostcode":"3000",
            "billingRegionName":"Victoria",
            "billingCountryName":"Australia",
            "billingCountryCodeISO2":"AU",
            "billingCountryCodeISO3":"AUS",
            "instructions":"Leave goods at the back entrance",
            "isDropship":"N", 
            "lines": jsonValue['lines']
        }
        result = {
            "version": 1.2,
            "resultStatus": 1,
            "message": "The purchase order data has been successfully obtained.",
            "dataTransferMode": "COMPLETE",
            "totalDataRecords": 1,
            "configs": {},
            "dataRecords": [parameter]
            }
        data = self.requests.post(purchaseURL, json=result, headers=header).json()
        # return the result code of purchase
        return data["result_code"], result
