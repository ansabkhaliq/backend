
from app.Resource.ProductResource import ProductResource
from app.Util import AuthUtil as authUtil

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
    return product_resource.get_product_by_barcode(barcode)


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
