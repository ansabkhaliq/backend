import logging
import datetime
import json
from app import config
from app.Resource.DatabaseBase import DatabaseBase
from app.Model.Order import Order
from app.Model.OrderDetail import OrderDetail

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class OrderResource(DatabaseBase):
    """
    A subclass of DatabaseBase, responsible for handling database
    operations regarding orders
    
    These operations include:
        - Storing a purchase made on SQUIZZ in the database
        - Retrieving order history
    """

    def __init__(self):
        super().__init__()



    # NOTE: This method will cause an exception because FK constraints fail due
    # to the supplier org ID being updated from PjSAS to HolySAS. Therefore, it
    # cannot store a purchase in the database yet
    def store_purchase(self, session_id: str, result_code: str, order: Order):
        """
        This methods will insert purchase table and lines tables in the database

        Args:
             session_id: SQUIZZ session ID for purchase submission
             result_code: response from SQUIZZ indicating purchase success or failure
             purchase_list: products listed in the purchase
        """
        now = datetime.datetime.now()
        dateTime = now.strftime("%Y-%m-%d  %H:%M:%S")
        supplierAccountCode = config.SUPPLIER_ORG_ID
        createdDate = dateTime
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
        orderDetails = [OrderDetail(entry) for entry in order.lines]
        for orderDetail in orderDetails:
            keyProductID = orderDetail.productId
            uri_search_query = "SELECT * FROM squizz_app.products WHERE keyProductID=%s"
            try:
                uri = self.run_query(uri_search_query, [keyProductID], False)
                orderDetail.uri_small  = uri[0]['uri_small']
                orderDetail.uri_medium = uri[0]['uri_medium']
                orderDetail.uri_large  = uri[0]['uri_large']
            except Exception as e:
                self.connection.rollback()
                logger.error('URI search error', e)

        insert_query = "INSERT INTO squizz_app.purchase(keyPurchaseOrderID, supplierAccountCode, " \
                       "customerAccountCode, keySupplierAccountID, createdDate, bill_status, " \
                       "deliveryContact, deliveryAddress1, deliveryAddress2, deliveryAddress3, session_id, line) " \
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = [
            order.keyPurchaseOrderID,
            supplierAccountCode,
            customerAccountCode,
            supplierAccountCode,
            createdDate,
            result_code,
            "+6144433332222",
            "Unit 5",
            "22 Bourkie Street",
            "Melbourne",
            session_id,
            json.dumps([orderDetail.__dict__ for orderDetail in orderDetails])
        ]
        try:
            self.run_query(insert_query, values, True)
        except Exception as e:
            self.connection.rollback()
            logger.error('Exception occurred when insert new purchase order', e)
        
        # insert table 'lines'
        try:
            for orderDetail in orderDetails:
                # insertion query for table 'lines'
                insert_query = "INSERT INTO squizz_app.lines(lineType, purchase_keyPurchaseOrderID, keyProductID,"\
                               "quantity, priceTotalExTax, products_id) VALUES (%s, %s, %s, %s, %s, %s)"
                values = [
                    orderDetail.lineType,
                    order.keyPurchaseOrderID,
                    orderDetail.productId,
                    orderDetail.quantity,
                    orderDetail.priceTotalExTax,
                    orderDetail.productId + config.SUPPLIER_ORG_ID
                ]
                try:
                    self.run_query(insert_query, values, True)
                except Exception as e:
                    self.connection.rollback()
                    failedToStore.append(orderDetail.productCode + "error:" + "failed to store the purchase of order")

        except Exception as e:
            logger.error('Exception occurred when insert new purchase order', e)
            result = {
                'status': "error",
                'data': 'null',
                'Message': 'Exception occurred when adding purchase order'
            }
            return result

        # Only 'SERVER_SUCCESS' means SQUIZZ accept the purchase, others are negative
        result = {
            'status': "success",
            'message': "successfully added the purchase orders",
            'data': {
                'puchaseID': order.keyPurchaseOrderID
            }
        }
        return result

        
    def history_order(self, session_id, date_time):
        """
        This method will return the last 15 history records from the search time
        Args: 
            session_id: session ID of current user
            data_time: start time of searching
        """
        customer_search_query = "SELECT customers_org_id FROM squizz_app.session WHERE id=%s"
        try:
            tempCustomer = self.run_query(customer_search_query, [session_id], False)
            customerAccountCode = tempCustomer[0]["customers_org_id"] # get cutomer organization ID
        except Exception as e:
            self.connection.rollback()
            logger.error('Session not found', e)
            result = {
                'status': "error",
                'data': 'null',
                'Message': 'Session invalid, please login again'
            }
            return result

        order_search_query = "SELECT keyPurchaseOrderID,createdDate,line," \
                             "bill_status FROM squizz_app.purchase WHERE " \
                             "customerAccountCode=%s and createdDate<=%s ORDER BY createdDate DESC LIMIT 15"
        try:
            order_info = self.run_query(order_search_query, [customerAccountCode, date_time], False)
            if order_info is not None:
                for i in range(0, len(order_info)):
                    order_info[i]['products'] = list(eval(order_info[i]['line']))
                    order_info[i].pop('line')

                result = {
                    'status': "success",
                    'message': "Successfully retrieved order history",
                    'data': {
                        'history_orders': order_info
                    }
                }
                return result
            else:
                result = {
                    'status': "success",
                    'data': 'null',
                    'message': "Success, but no data found!"
                }
                return result
        except Exception as e:
            logger.error('Could not retrieve order history:', e)
            result = {
                'status': "error",
                'data': 'null',
                'Message': 'Exception occurred when retrieving history order' + str(e)
            }
            return result
