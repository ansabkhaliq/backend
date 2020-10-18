from app.Model.CateProd import CateProd
from app.Model.Category import Category
from app.Model.Price import Price
from app.Resource.SimpleModelResource import SimpleModelResource as SR
from app.Resource.ProductResource import ProductResource
from app.Util import AuthUtil as authUtil
from app.Model.Product import Product


def retrieve_products(customer_code="TESTDEBTOR") -> dict:
    connection = authUtil.build_connection()
    data_type = 3
    success, product_list = connection.retrieve_organisation_data(data_type, customer_code=customer_code)
    product_resource = ProductResource()
    if success:
        return product_resource.store_products(product_list)

    return {
        'status': "error",
        'data': 'null',
        'Message': "Error while retrieving products data from server"
    }


def retrieve_prices() -> dict:
    connection = authUtil.build_connection()
    data_type = 37
    success, price_list = connection.retrieve_organisation_data(data_type)
    product_resource = ProductResource()
    if success:
        return product_resource.store_prices(price_list)

    return {
        'status': 'error', 
        'data': 'null', 
        'Message': 'Error while retrieving product prices data from server'
    }


def get_product_by_barcode(barcode) -> dict:
   
    # Get Product Details
    product_resource = ProductResource()
    product_record = product_resource.get_product_by_barcode(barcode)


    try:
        if product_record is not None:
            # Get Product images
            image_records = get_product_images(product_record['id'])

            # Converting Decimal to float (Python serializable)
            product_record['price'] = float(product_record['price'])


            # Packing data in the Model
            product_record = Product(product_record)
            if image_records is not None:
                product_record.imageList = image_records[0]

            result = {
                'status': "success",
                'message': "successfully retrieved product",
                'data': product_record.__dict__
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
            'data': 'null',
            'Message': str(e)
        }

    return result


def get_product_by_product_code(productCode) -> dict:

    # Get Product Details
    pr = ProductResource()
    product_record = pr.get_product_by_product_code(productCode)


    try:
        if product_record is not None:
            # Get Product images
            image_records = get_product_images(product_record['id'])

            # Converting Decimal to float (Python serializable)
            product_record['price'] = float(product_record['price'])


            # Packing data in the Model
            product_record = Product(product_record)
            if image_records is not None:
                product_record.imageList = image_records
            
            result = {
                'status': "success",
                'message': "successfully retrieved product",
                'data': product_record.__dict__
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
            'data': 'null',
            'Message': str(e)
        }

    return result


def get_product_images(id) -> dict:
    product_resource = ProductResource()
    image_records = product_resource.get_product_images_by_id(id)
    return image_records


def update_products() -> dict:
    product_resource = ProductResource()
    connection = authUtil.build_connection()
    data_type = 3
    success, product_list = connection.retrieve_organisation_data(data_type)

    if success:
        return product_resource.update_products(product_list)
    
    return {
        'status': 'error',
        'data': 'null',
        'Message': 'Error while retrieving product from server'
    }


def update_prices(customer_code='TESTDEBTOR') -> dict:
    connection = authUtil.build_connection()
    data_type = 37
    success, price_list = connection.retrieve_organisation_data(data_type, customer_code)
    product_resource = ProductResource()

    if success:
        return product_resource.update_prices(price_list)

    return {
        'status': 'error',
        'data': 'null',
        'Message': "Error while retrieving product price from SQUIZZ server"
    }


def restore_category():
    connection = authUtil.build_connection()
    status, categories = connection.retrieve_organisation_data(8)

    if not status:
        return {
            'status': 'Failed',
            'message': 'Retrieve data from squizz failed.'
        }

    sr = SR()
    try:
        # Rewrite categories
        sr.truncate(CateProd, False)
        sr.truncate(Category, False)
        sr.batch_insert(categories, commit=False)

        # Traverse products and convert to key, id pairs
        prod_key_id = {}
        for product in sr.list_all(Product):
            prod_key_id[product.keyProductID] = product.id

        # Rewrite category product relationships
        for category in categories:
            if category.keyCategoryParentID is None:
                continue
            if category.keyProductIDs is None:
                continue
            print(category.keyProductIDs)
            for productKey in category.keyProductIDs:
                cate_prod_rel = CateProd({'categoryId': category.id, 'productId': prod_key_id[productKey]})
                sr.insert(cate_prod_rel, commit=False)

    except Exception as e:
        sr.connection.rollback()
        sr.cursor.close()
        raise e
    else:
        sr.connection.commit()
        sr.cursor.close()

    return {
        'status': 'Success',
        'message': 'Category data Updated'
    }


def restore_prices(customer_code="TESTDEBTOR"):
    connection = authUtil.build_connection()
    status, prices = connection.retrieve_organisation_data(37, customer_code)
    if not status:
        return {
            'status': 'Failed',
            'message': 'Retrieve data from squizz failed.'
        }

    sr = SR()
    try:
        # Truncate prices
        sr.truncate(Price, False)

        # Traverse products and convert to key, id pairs
        prod_key_id = {}
        for product in sr.list_all(Product, ['keyProductId', 'id']):
            prod_key_id[product.keyProductID] = product.id

        # Rewrite prices
        for price in prices:
            price.productId = prod_key_id[price.keyProductID]
            sr.insert(price, False)

    except Exception as e:
        sr.connection.rollback()
        sr.cursor.close()
        raise e
    else:
        sr.connection.commit()
        sr.cursor.close()

    return {
        'status': 'Success',
        'message': 'Price data Updated.'
    }
