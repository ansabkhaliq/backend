import logging
import datetime
from app import config
from app.Resource.DatabaseBase import DatabaseBase
from app.Model.Product import Product
from app.Model.Price import Price
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ProductResource(DatabaseBase):
    """
    A subclass of DatabaseBase, responsible for handling database
    operations regarding products
    
    These operations include:
        - Product insertion
        - Product price insertion
        - Retrieving barcode values
        - Batch synchronizing product data with the SQUIZZ platform
        - Batch synchronizing product prices with the SQUIZZ platform
    """

    def __init__(self):
        super().__init__()


    def store_products(self, product_list: List[Product]):
        insert_query = "INSERT INTO products(id, keyTaxCodeID, supplierAccountCode, " \
                       "productCode, keyProductID, barcode, barcodeInner, name," \
                       "description1, keySellUnitID, width, height, stockQuantity," \
                       "stockLowQuantity, isPriceTaxInclusive, isKitted, kitProductsSetPrice, internalID)" \
                       " VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s,%s,%s) "

        failedToStore = []
        for product in product_list:
            try:
                values = [
                    product.keyProductID + config.SUPPLIER_ORG_ID,
                    product.keyTaxcodeID,
                    config.SUPPLIER_ORG_ID,
                    product.productCode,
                    product.keyProductID,
                    product.barcode,
                    product.barcodeInner,
                    product.name,
                    product.description1,
                    product.keySellUnitID,
                    product.width,
                    product.height,
                    product.stockQuantity,
                    product.stockLowQuantity,
                    product.isPriceTaxInclusive,
                    product.isKitted,
                    product.kitProductsSetPrice,
                    product.internalID
                ]
                self.run_query(insert_query, values, True)

            except Exception as e:
                logger.error("exception", e)
                failedToStore.append(product.keyProductID + "error: " + str(e))

        logger.info('completed store_products')
        result = {
            'status': "success",
            'message': "successfully stored products",
            'data': {
                'failed': failedToStore
            }, 
        }
        return result

    
    def store_prices(self, price_list: List[Price]):
        insert_query = "INSERT INTO squizz_app.price_level(products_id, keySellUnitID, "\
                      "referenceId, referenceType, price, keyProductID, date_time)"\
                      " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        search_query = "SELECT * FROM products WHERE keyProductID=%s"
        failedToStore = []
        for price in price_list:
            # First, search in the product table to check whether this product exsts.
            # If not, skip this record and continue. Otherwise, it may cause foreign key
            # constraint issue
            product_record = None
            try:
                product_record = self.run_query(search_query, price.keyProductID, False)
            except Exception as e:
                logger.error('Exception occurred when searching for product record in store_product_level method.', e)

            if product_record is not None:
                # Since we already checked the existence of the product, we could do the insertion.
                try:
                    now = datetime.datetime.now()
                    dateTime = now.strftime("%Y-%m-%d  %H:%M:%S")
                    values = [
                        price.keyProductID + config.SUPPLIER_ORG_ID,
                        price.keySellUnitID,
                        price.referenceID,
                        price.referenceType,
                        price.price,
                        price.keyProductID,
                        dateTime
                    ]
                    self.run_query(insert_query, values, True)
                except Exception as e:
                    logger.error("Exception", e)
                    failedToStore.append(price.keyProductID + "error: " + str(e))
            else:
                failedToStore.append(price.keyProductID + " error:" + " product does not exist")

        logger.info('completed store_prices')
        result = {
            'status': 'success',
            'message': 'successfully stored product pricess',
            'data': {
                'failed': failedToStore
            }
        }
        return result


    def get_product_by_barcode(self, barcode):
        sql_query = "SELECT * FROM squizz_app.products RIGHT JOIN "\
                    "squizz_app.price_level ON squizz_app.products.id=squizz_app.price_level.products_id " \
                    "WHERE squizz_app.products.barcode = %s"
        values = self.run_query(sql_query % barcode, [], False)
        try:
            if values is not None:
                product = values[0]
                result = {
                    'status': "success",
                    'message': "successfully retrieved product",
                    'data': {
                        'productname': product['name'],
                        'keyProductCode': product['keyProductID'],
                        'price': product['price'],
                        'filename': product['filename'],
                        'uri_small': product['uri_small'],
                        'uri_medium': product['uri_medium'],
                        'uri_large': product['uri_large'],
                        'productCode': product['productCode']
                    }
                }
            else:
                result = {
                    'status': "error",
                    'data': 'null',
                    'Message': "No data found"
                }
        except Exception as e:
            result = {
                'status': "error",
                'data':'null', 
                'Message': str(e)
            }

        return result


    def update_products(self, product_list: List[Product]):
        """
        Takes as input the retrieved product data from SQUIZZ API, then
        synchronises the data with the current records stored in the database.
        If they are not identical, it will update the product information 
        to the latest one.

        Args:
            product_list: list of Product objects created from data retrieved from SQUIZZ API
        """
        value_not_inserted = 0
        value_inserted = 0

        # the primary keys of the product table is 'id' which is automatically generated by local database, can not
        # included in the json_value. Therefore, we use the 'keyProductID' to do the query
        failedToStore = []
        for product in product_list:
            search_query = "SELECT id, keyTaxCodeID, supplierAccountCode, " \
                           "keyProductID, barcode, barcodeInner, name," \
                           "description1, keySellUnitID, width, height, " \
                           "stockQuantity, stockLowQuantity, isPriceTaxInclusive, " \
                           "isKitted, kitProductsSetPrice, internalID " \
                           "FROM products " \
                           "WHERE keyProductID=%s"
            result = None
            try:
                # TODO: discuss later, theoretically, there ought to be only one record. Attention: the record retrieved below
                result_all = self.run_query(search_query, product.keyProductID, False)
                result = result_all[0]
            except Exception as e:
                value_not_inserted += 1
                logger.error('Exception occurred when searching for record in update product session', e)
                failedToStore.append(product.keyProductID + " error:" + " product does not exist")

            if not result:
                logger.error('Get no corresponding record, insert a new record.')
                # TODO: insert a new record, how to handle the auto-increased id in local db,
                #  currently we use store_product method
                self.store_products([product])
                value_inserted += 1

            else:
                latest_record = [
                    product.keyProductID + config.SUPPLIER_ORG_ID,
                    product.keyTaxcodeID,
                    config.SUPPLIER_ORG_ID,
                    product.keyProductID,
                    product.barcode,
                    product.barcodeInner,
                    product.name,
                    product.description1,
                    product.keySellUnitID,
                    product.width,
                    product.height,
                    product.stockQuantity,
                    product.stockLowQuantity,
                    product.isPriceTaxInclusive,
                    product.isKitted,
                    product.kitProductsSetPrice,
                    product.internalID,
                    product.productCode
                ]

                # TODO: Currently, for simplicity, we just update the entire record once it is inconsistent with the
                #  latest record
                latest_record.append(product.keyProductID)
                # latest_record = tuple(latest_record)
                update_query = "UPDATE products " \
                               "SET id = %s, keyTaxCodeID=%s, supplierAccountCode=%s," \
                               "keyProductID=%s, barcode=%s, barcodeInner=%s, name=%s," \
                               "description1=%s, keySellUnitID=%s, width=%s, height=%s," \
                               "stockQuantity=%s, stockLowQuantity=%s, isPriceTaxInclusive=%s," \
                               "isKitted=%s, kitProductsSetPrice=%s, internalID=%s, productCode=%s " \
                               "WHERE keyProductID=%s"

                try:
                    self.run_query(update_query, latest_record, True)
                    value_inserted += 1
                except Exception as e:
                    self.connection.rollback()
                    logger.error('Exception occurred when updating product table', e)
                    value_not_inserted += 1
                    failedToStore.append(product.keyProductID + " error:" + " error occured while updating: " + str(e))

        self.connection.close()
        logger.info('This is the value updated: %d' % value_inserted)
        logger.info('This is the value not updated: %d' % value_not_inserted)
        result = {'status': "success", 'data': {'failed':failedToStore}, 'message': "successfully updated products"}
        logger.info('Successfully synchronized latest products data from the SQUIZZ API')
        return result


    def update_prices(self, price_list: List[Price]):
        """
        Updates the 'price_level' table in the database. It compares the 
        retrieved price data from the SQUIZZ API with data in the application
        database. If they are identical, it only updates datetime. otherwise, 
        the entire record will be updated.

        Args:
            price_list: list of Price objects created from data retrieved from SQUIZZ API
        """
        failedToStore = []
        for price in price_list:
            search_query = "SELECT products_id, keySellUnitID, "\
                           "referenceId, referenceType, price, date_time " \
                           "FROM price_level " \
                           "WHERE keyProductID = %s"
            try:
                result_all = self.run_query(search_query, price.keyProductID, False)
                if result_all is None:
                    self.store_product_price([price])
                else:
                    current_time = datetime.datetime.now()
                    date_time = current_time.strftime("%Y-%m-%d  %H:%M:%S")
                    latest_values = [
                        price.keyProductID + config.SUPPLIER_ORG_ID,
                        price.keySellUnitID,
                        price.referenceID,
                        price.referenceType,
                        price.price,
                        date_time,
                        price.keyProductID
                    ]
                    update_query = "UPDATE price_level " \
                                   "SET products_id=%s, keySellUnitID=%s, referenceId=%s, " \
                                   "referenceType=%s, price= %s, date_time=%s " \
                                   "WHERE keyProductID = %s"
                    try:
                        self.run_query(update_query, latest_values, True)
                    except Exception as e:
                        self.connection.rollback()
                        logger.error('Exception occurred when updating the latest price info', e)
                        failedToStore.append(price.keyProductID + "error:" + "failed to update price")

            except Exception as e:
                logger.error('Exception occurred when search price in price_level', e)
                failedToStore.append(price.keyProductID + "error:" + "failed to update price")
                
        logger.info("Successfully updated 'price_level' table")
        result = {
            'status': "success",
            'message': "successfully updated product prices",
            'data': {
                'failed':failedToStore
            },
        }
        return result

    
