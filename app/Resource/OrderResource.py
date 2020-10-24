import logging
import datetime
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

    def store_purchase(self, session_id: str, result_code: str, order: Order):
        """
        This methods will insert purchase table and lines tables in the database

        Args:
             session_id: SQUIZZ session ID for purchase submission
             result_code: response from SQUIZZ indicating purchase success or failure
             purchase_list: products listed in the purchase
        """
        
        # Search the user organization ID based on session ID from sessions table
        organization_id = None
        search_query = """SELECT organizations.id AS org_id 
                          FROM sessions INNER JOIN organizations
                          ON organizations.Id = sessions.OrganizationId
                          WHERE SessionKey=%s"""
        try:
            result = self.run_query(search_query, [session_id], False)
            if result:
                organization_id = result[0]['org_id']
        except Exception as e:
            self.connection.rollback()
            logger.error(f'Could not find session with ID {session_id}', e)

        # Insert the order into the 'orders' table
        insert_query = ( 
        """INSERT into orders (SupplierOrganizationId, CreatedOnDate, 
           Instructions, DeliveryOrganizationName, DeliveryContact, DeliveryEmail,
           DeliveryAddress1, DeliveryAddress2, DeliveryAddress3, DeliveryRegionName,
           DeliveryCountryName, DeliveryPostCode, BillingContact, BillingEmail,
           BillingOrganizationName, BillingAddress1, BillingAddress2, BillingAddress3,
           BillingRegionName, BillingCountryName, BillingPostCode, IsDropship, BillStatus, OrganizationId)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

        values = [
            config.SUPPLIER_ORG_ID,
            datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),
            order.instructions,
            order.deliveryOrgName,
            order.deliveryContact,
            order.deliveryEmail,
            order.deliveryAddress1,
            order.deliveryAddress2,
            order.deliveryAddress3,
            order.deliveryRegionName,
            order.deliveryCountryName,
            order.deliveryPostcode,
            order.billingContact,
            order.billingEmail,
            order.billingOrgName,
            order.billingAddress1,
            order.billingAddress2,
            order.billingAddress3,
            order.billingRegionName,
            order.billingCountryName,
            order.billingPostcode,
            order.isDropship,
            result_code,
            organization_id
        ]

        try:
            self.run_query(insert_query, values, True)
        except Exception as e:
            self.connection.rollback()
            logger.error('Exception occurred when inserting order', e)

        # Get the id of the inserted order
        orderId = self.cursor.lastrowid
        order.id = orderId

        # Insert each item (and associated info) in the order into the 'orderdetails' table
        failedToStore = []
        orderDetails = [OrderDetail(entry) for entry in order.lines]  # Lines are equal to order details
        try:
            for orderDetail in orderDetails:
                # Set the orderID field for order detail
                orderDetail.orderId = orderId

                # Retrieve the product ID from 'products' table and set it
                # within the orderDetail object
                search_query = """SELECT id, productName, productCode
                                  FROM products WHERE keyProductId=%s"""
                values = [orderDetail.keyProductID]
                try:
                    product = self.run_query(search_query, values, True)[0]
                    if product:
                        orderDetail.productId = product['id']
                        orderDetail.productName = product['productName']
                        orderDetail.productCode = product['productCode']
                except Exception as e:
                    self.connection.rollback()
                    failedToStore.append(orderDetail.productCode + "error:" +
                                         f" could not find product with keyProductID {orderDetail.keyProductID}")
                    continue
                
                # Insert an order detail record for the product in the order
                insert_query = (
                    """INSERT into orderdetails (KeyProductId, ProductName,
                       Quantity, UnitPrice, TotalPrice, TotalPriceIncTax, 
                       TotalPriceExTax, ProductCode, OrderId, ProductId)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

                values = [
                    orderDetail.keyProductID,
                    orderDetail.productName,
                    orderDetail.quantity,
                    orderDetail.unitPrice,  # Is null for now since SQUIZZ is not returning unitPrice in JSON, however, unit prices are found in totalPriceExTax field in DB
                    orderDetail.totalPrice,
                    orderDetail.priceTotalIncTax,
                    orderDetail.priceTotalExTax,
                    orderDetail.productCode,
                    orderDetail.orderId,
                    orderDetail.productId
                ]

                try:
                    self.run_query(insert_query, values, True)
                except Exception as e:
                    self.connection.rollback()
                    failedToStore.append(orderDetail.productCode + "error:" + " failed to store order detail for product")

        except Exception as e:
            logger.error('Exception occurred when inserting order details', e)
            result = {
                'status': "error",
                'data': failedToStore,
                'message': 'Exception occurred when inserting order details'
            }
            return result

        result = {
            'status': "success",
            'message': "Successfully inserted order and order details",
            'data': {
                'purchaseID': order.id
            }
        }
        return result
        
    def get_order_history(self, session_id):
        """
        This method will return all order records from the database

        Args:
            session_id: session ID of current authenticated user
        """
        # Search the user organization ID based on session ID from sessions table
        organizationId = None
        search_query = """SELECT organizations.id AS org_id 
                          FROM sessions INNER JOIN organizations
                          ON organizations.Id = sessions.OrganizationId
                          WHERE sessionKey=%s"""
        try:
            result = self.run_query(search_query, [session_id], False)
            if result:
                organizationId = result[0]['org_id']

        except Exception as e:
            self.connection.rollback()
            logger.error(f'Could not find session with ID {session_id}', e)
            result = {
                'status': 'error',
                'orders': None,
                'message': 'Invalid session, please try login again'
            }
            return result
            
        # Retrieve the organization's previous 50 orders
        search_query = """SELECT * FROM orders WHERE organizationId = %s
                          ORDER BY createdOnDate DESC LIMIT 50"""
        
        values = [organizationId]
        try:
            # For each order, get associated order detail records
            orders = self.run_query(search_query, values, False)
            for order in orders:
                order_id = order['id']
                search_query = "SELECT * FROM orderdetails WHERE OrderId = %s"
                values = [order_id]
                try:
                    order_details = self.run_query(search_query, values, False)
                    order['lines'] = order_details
                except Exception as e:
                    logger.error(f'Could not retrieve order details for order ID {order_id}')
            
            result = {
                'status': 'success',
                'message': 'Successfully retrieved order history',
                'orders': orders
            }
        except:
            logger.error('Could not retrieve order history')
            result = {
                'status': 'error',
                'orders': None,
                'message': 'Exception occurred when retrieving order history'
            }

        return result

    def save_order(self, customer, delivery_address, billing_address, products_list):
        pass
