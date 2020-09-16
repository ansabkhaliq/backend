import logging
import datetime
from app import config
from app.Resource.DatabaseBase import DatabaseBase
from app.Model.Product import Product
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


    def store_product(self, productList: List[Product]):
        value_not_inserted = 0
        value_inserted = 0
        insert_query = "INSERT INTO products(id, keyTaxCodeID, supplierAccountCode, " \
                       "productCode, keyProductID, barcode, barcodeInner, name," \
                       "description1, keySellUnitID, width, height, stockQuantity," \
                       "stockLowQuantity, isPriceTaxInclusive, isKitted, kitProductsSetPrice, internalID)" \
                       " VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s,%s,%s) "

        failedToStore = []
        for product in productList:
            try:
                values = [
                    # dataRecord['keyProductID'] + config.SUPPLIER_ORG_ID,
                    # dataRecord['keyTaxcodeID'], 
                    # config.SUPPLIER_ORG_ID,
                    # dataRecord['productCode'],
                    # dataRecord['keyProductID'],
                    # dataRecord['barcode'],
                    # dataRecord['barcodeInner'],
                    # dataRecord['name'],
                    # dataRecord['description1'],
                    # dataRecord['keySellUnitID'],
                    # dataRecord['width'],
                    # dataRecord['height'],
                    # dataRecord['stockQuantity'],
                    # dataRecord['stockLowQuantity'],
                    # dataRecord['isPriceTaxInclusive'],
                    # dataRecord['isKitted'],
                    # dataRecord['kitProductsSetPrice'],
                    # dataRecord['internalID']
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

        logger.info('completed store_product')
        result = {'status': "success", 'data': {'failed': failedToStore}, 'message': "successfully stored products"}
        return result

    
    def store_product_price(self, jsonValue):
        insert_query = "INSERT INTO squizz_app.price_level(products_id, keySellUnitID, "\
                      "referenceId, referenceType, price, keyProductID, date_time)"\
                      " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        search_query = "SELECT * FROM products WHERE keyProductID=%s"
        failedToStore = []
        for dataRecord in jsonValue:
            #print(dataRecord)
            key_product_id = dataRecord['keyProductID']
            # First, search in the product table to check whether this product exsts.
            # If not, skip this record and continue. Otherwise, it may cause foreign key
            # constraint issue.
            product_record = None
            try:
                #self.cursor.execute(search_query, key_product_id)
                #_, product_record = self.cursor.fetchall()
                product_record = self.run_query(search_query, key_product_id, False)
            except Exception as e:
                logger.error('Exception occurred when searching for product record in store_product_level method.', e)

            if product_record is not None:
                # Since we already checked the existence of the product, we could do the insertion.
                try:
                    now = datetime.datetime.now()
                    dateTime = now.strftime("%Y-%m-%d  %H:%M:%S")
                    values = [
                        dataRecord['keyProductID'] + config.SUPPLIER_ORG_ID, 
                        dataRecord['keySellUnitID'],
                        dataRecord['referenceID'],
                        dataRecord['referenceType'],
                        dataRecord['price'],
                        dataRecord['keyProductID'],
                        dateTime
                    ]
                    self.run_query(insert_query, values, True)
                except Exception as e:
                    logger.error("Exception", e)
                    failedToStore.append(dataRecord['keyProductID']+ "error: " + str(e))

            else:
                failedToStore.append(dataRecord['keyProductID'] + "error:" + "product does not exist")

        logger.info('completed store_product_price')
        result = {'status': "success", 'data': {'failed':failedToStore}, 'message': "successfully stored price of products"}
        return result


    def get_product_by_barcode(self, barcode):
        sql_query = "SELECT * FROM squizz_app.products RIGHT JOIN squizz_app.price_level ON squizz_app.products.id=squizz_app.price_level.products_id " \
                    "WHERE squizz_app.products.barcode = %s"
        values = self.run_query(sql_query % barcode,[], False)
        print(values)
        try:
            if values is not None:
                result = {'status': "success", 'data': {'productname': values[0]['name'], 'keyProductCode': values[0]['keyProductID'], 'price': values[0]['price'],'filename':values[0]['filename'],
                                                        'uri_small':values[0]['uri_small'],'uri_medium':values[0]['uri_medium'],'uri_large':values[0]['uri_large'], 'productCode': values[0]['productCode']}, 
                                                        'message': "successfully retrieved price"}
                return result
            else:
                result = {'status': "error",'data': 'null', 'Message': "No data found"}
                return result
        except Exception as e:
            result = {'status': "error",'data':'null', 'Message': str(e)}
            return result


    def update_product(self, json_values):
        """
        This method retrieves the product data from SQUIZZ API every 24 hour, it then checks with the local database.
        If they are not identical, it will update the product information to the latest one.

        Args:
            json_values - the json records of product information retrieved through SQUIZZ API
        """
        value_not_inserted = 0
        value_inserted = 0

        # the primary keys of the product table is 'id' which is automatically generated by local database, can not
        # included in the json_value. Therefore, we use the 'keyProductID' to do the query
        failedToStore = []
        for data_record in json_values:
            key_product_id = data_record['keyProductID']
            search_query = "SELECT id, keyTaxCodeID, supplierAccountCode, " \
                           "keyProductID, barcode, barcodeInner, name," \
                           "description1, keySellUnitID, width, height, " \
                           "stockQuantity, stockLowQuantity, isPriceTaxInclusive, " \
                           "isKitted, kitProductsSetPrice, internalID " \
                           "FROM products " \
                           "Where keyProductID=%s"
            result = None
            try:
                # TODO: discuss later, theoretically, there ought to be only one record. Attention: the record retrieved below
                result_all = self.run_query(search_query, key_product_id, False)
                result = result_all[0]
            except Exception as e:
                value_not_inserted += 1
                logger.error('Exception occurred when searching for record in update product session', e)
                failedToStore.append(data_record['keyProductID'] + "error:" + "product does not exist")

            if result is None:
                logger.error('Get no corresponding record, insert a new record.')
                # TODO: insert a new record, how to handle the auto-increased id in local db,
                #  currently we use store_product method
                json_value = [data_record]
                self.store_product(json_value)
                value_inserted += 1

            else:
                latest_record = [
                    data_record['keyProductID'] + config.SUPPLIER_ORG_ID,
                    data_record['keyTaxcodeID'],
                    config.SUPPLIER_ORG_ID,
                    data_record['keyProductID'],
                    data_record['barcode'],
                    data_record['barcodeInner'],
                    data_record['name'],
                    data_record['description1'],
                    data_record['keySellUnitID'],
                    data_record['width'],
                    data_record['height'],
                    data_record['stockQuantity'],
                    data_record['stockLowQuantity'],
                    data_record['isPriceTaxInclusive'],
                    data_record['isKitted'],
                    data_record['kitProductsSetPrice'],
                    data_record['internalID'],
                    data_record['productCode']
                ]

                # TODO: Currently, for simplicity, we just update the entire record once it is inconsistent with the
                #  latest record
                latest_record.append(key_product_id)
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
                    failedToStore.append(data_record['keyProductID'] + "error:" + "error occured while updating: " + str(e))

        self.connection.close()
        logger.info('This is the value updated: %d' % value_inserted)
        logger.info('This is the value not updated: %d' % value_not_inserted)
        result = {'status': "success", 'data': {'failed':failedToStore}, 'message': "successfully updated products"}
        return result
    logger.info('Successfully retrieved and synchronized latest products data from the SQUIZZ API')


    def update_product_price(self, json_values):
        """
        This methods updates price_level table every 24 hours.
        It compares the retrieved data with data in the local database. If they are identical, it only updates datetime;
        otherwise, the entire record will be updated.

        Args:
             json_values - the json records of product price retrieved through SQUIZZ API
        """
        failedToStore = []
        for data_record in json_values:
            key_product_id = data_record['keyProductID']
            search_query = "SELECT products_id, keySellUnitID, "\
                           "referenceId, referenceType, price, date_time " \
                           "FROM price_level " \
                           "WHERE keyProductID = %s"
            try:
                result_all = self.run_query(search_query, key_product_id, False)
                if result_all is None:
                    json_value = [data_record]
                    self.store_product_price(json_value)
                else:
                    current_time = datetime.datetime.now()
                    date_time = current_time.strftime("%Y-%m-%d  %H:%M:%S")
                    latest_values = [
                        data_record['keyProductID'] + config.SUPPLIER_ORG_ID,
                        data_record['keySellUnitID'],
                        data_record['referenceID'],
                        data_record['referenceType'],
                        data_record['price'],
                        date_time,
                        data_record['keyProductID']
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
                        failedToStore.append(data_record['keyProductID'] + "error:" + "failed to update price")
            except Exception as e:
                logger.error('Exception occurred when search price in price_level', e)
                failedToStore.append(data_record['keyProductID'] + "error:" + "failed to update price")
                # self.connection.close()
        result = {'status': "success", 'data': {'failed':failedToStore}, 'message': "successfully updated price of products"}
        return result
    logger.info("Successfully updated 'price_level' table")
