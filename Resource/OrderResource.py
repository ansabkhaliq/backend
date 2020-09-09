import logging
import datetime
from .DatabaseResource import DatabaseResource

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class OrderResource(DatabaseResource):
    """
    A subclass of DatabaseResource, responsible for handling database
    operations regarding orders
    
    These operations include:
        - Creating a purchase and synchronizing the purchase with SQUIZZ
        - Retrieving order history
    """

    def __init__(self):
        super().__init__()


    def purchase(self, session_id, squizzResp, purchaseList):
        """
        This methods will insert purchase table and lines tables in the database

        Args:
             session_id: squizz session id for submit purchase
             squizzResp: response from SQUIZZ indicating whether the purchase has been proceeded successfully
             purchaseList: products listed in the purchase
        """
        now = datetime.datetime.now()
        dateTime = now.strftime("%Y-%m-%d  %H:%M:%S")
        PjSAS_id = "11EA0FDB9AC9C3B09BE36AF3476460FC"

        keyPurchaseOrderID = purchaseList['dataRecords'][0]['keyPurchaseOrderID']
        supplierAccountCode = PjSAS_id
        createdDate = dateTime
        status = squizzResp
        failedToStore = []

        # search the user organization ID based on session ID from seesion table
        search_query = "SELECT customers_org_id FROM squizz_app.session WHERE id=%s"
        try:
            tempCustomer = self.run_query(search_query, [session_id], False)
            # get cutomer organization ID
            customerAccountCode = tempCustomer[0]["customers_org_id"]
        except Exception as e:
            self.connection.rollback()
            logger.error('Session not found', e)
        # Insert the purchase records. lines are store as strings in this table for fast lookup.
        lines = purchaseList['dataRecords'][0]["lines"]
        for i in range(0, len(lines)):
            keyProductID = lines[i]["productId"]
            uri_search_query = "SELECT * FROM squizz_app.products WHERE keyProductID=%s"
            try:
                uri = self.run_query(uri_search_query, [keyProductID], False)
                lines[i]['uri_small'] = uri[0]['uri_small']
                lines[i]['uri_medium'] = uri[0]['uri_medium']
                lines[i]['uri_large'] = uri[0]['uri_large']
            except Exception as e:
                self.connection.rollback()
                logger.error('URI search error', e)

        insert_query = "INSERT INTO squizz_app.purchase(keyPurchaseOrderID, supplierAccountCode, "\
                      "customerAccountCode, keySupplierAccountID, createdDate, bill_status, "\
                      "deliveryContact, deliveryAddress1, deliveryAddress2, deliveryAddress3, session_id, line)"\
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = [
            keyPurchaseOrderID, supplierAccountCode, customerAccountCode, supplierAccountCode,
            createdDate, status, 
            "+6144433332222", "Unit 5", "22 Bourkie Street", "Melbourne",  # Hard code variables
            session_id, str(lines)
        ]
        try:
            self.run_query(insert_query, values, True)
        except Exception as e:
            self.connection.rollback()
            logger.error('Exception occurred when insert new purchase order', e)
        
        # insert table 'lines'
        try:
            for line in lines:
                # insertion query for table 'lines'
                insert_query = "INSERT INTO squizz_app.lines(lineType, purchase_keyPurchaseOrderID, keyProductID,"\
                               "quantity, priceTotalExTax, products_id) VALUES (%s, %s, %s, %s, %s, %s)"
                values = [
                    line['lineType'], keyPurchaseOrderID, line['productId'], line['quantity'],
                    line['priceTotalExTax'], line['productId'] + PjSAS_id
                ]
                try:
                    self.run_query(insert_query, values, True)
                except Exception as e:
                    self.connection.rollback()
                    failedToStore.append(line['productCode'] + "error:" + "failed to store the purchase of order")

        except Exception as e:
            logger.error('Exception occurred when insert new purchase order', e)
            result = {'status': "error", 'data': 'null',
                      'Message': 'Exception occurred when adding purchase order'}
            return result

        # Only 'SERVER_SUCCESS' means SQUIZZ accept the purchase, others are negative
        result = {'status': "success", 'data': {'puchaseID':keyPurchaseOrderID}, 'message': "successfully added the purchase orders"}
        return result

        
    def history_order(self, session_id, date_time):
        """
        This method will return the last 15 history records from the search time
        Args: 
            session_id: session ID of current user.
            data_time: start time of searching
        """
        customer_search_query = "SELECT customers_org_id FROM squizz_app.session WHERE id=%s"
        try:
            tempCustomer = self.run_query(customer_search_query, [session_id], False)
            customerAccountCode = tempCustomer[0]["customers_org_id"] # get cutomer organization ID
        except Exception as e:
            self.connection.rollback()
            logger.error('Session not found', e)
            result = {'status': "error", 'data': 'null','Message': 'Session invalid, please login again'}
            return result
        # query for searching the history orders
        order_search_query = "SELECT keyPurchaseOrderID,createdDate,line," \
                             "bill_status FROM squizz_app.purchase WHERE " \
                             "customerAccountCode=%s and createdDate<=%s ORDER BY createdDate DESC LIMIT 15"
        try:
            order_info = self.run_query(order_search_query, [customerAccountCode, date_time], False)
            if order_info is not None:
                for i in range(0, len(order_info)):
                    order_info[i]['products'] = list(eval(order_info[i]['line']))
                    order_info[i].pop('line')
                result = {'status': "success", 'data': {'history_orders': order_info}, 'message': "successfully retrieved history order"}
                return result
            else:
                result = {'status': "success", 'data': 'null', 'message': "Success, but no data found!"}
                return result
        except Exception as e:
            logger.error('Order searching failure:', e)
            result = {'status': "error", 'data': 'null','Message': 'Exception occurred when retrieving history order' +str(e)}
            return result
