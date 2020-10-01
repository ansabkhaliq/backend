
from app.Resource.ProductResource import ProductResource
from app.Util import AuthUtil as authUtil
from app.Model.Product import Product

product_resource = ProductResource()


def retrieve_products() -> dict:
    connection = authUtil.build_connection()
    data_type = 3
    success, product_list = connection.retrieve_organisation_data(data_type)
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

    if success:
        return product_resource.store_prices(price_list)

    return {
        'status': 'error', 
        'data': 'null', 
        'Message': 'Error while retrieving product prices data from server'
    }


def get_product_by_barcode(barcode) -> dict:
   
    # Get Product Details
    product_record = product_resource.get_product_by_barcode(barcode)

    # Get Product images
    image_records = get_product_images(product_record['id'])
    try:
        if product_record is not None:


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
    product_record = product_resource.get_product_by_product_code(productCode)

    # Get Product images
    image_records = get_product_images(product_record['id'])
    try:
        if product_record is not None:


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


def get_product_images(id) -> dict:
    image_records = product_resource.get_product_images_by_id(id)
    return image_records


def update_products() -> dict:
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


def update_prices() -> dict:
    connection = authUtil.build_connection()
    data_type = 37
    success, price_list = connection.retrieve_organisation_data(data_type)

    if success:
        return product_resource.update_prices(price_list)

    return {
        'status': 'error',
        'data': 'null',
        'Message': "Error while retrieving product price from SQUIZZ server"
    }
