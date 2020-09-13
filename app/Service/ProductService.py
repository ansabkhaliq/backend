
from Resource.ProductResource import ProductResource
from app.Util import AuthUtil as authUtil

product_resource = ProductResource()


def retrieve_product() -> dict:
    connection = authUtil.build_connection()
    data_type = 3
    jsonResponse, jsonValues = connection.get_product_list(data_type)
    if jsonResponse:
        return product_resource.store_product(jsonValues)

    else:
        return {'status': "error", 'data': 'null', 'Message': "Error while retrieving product from server"}


def retrieve_product_price() -> dict:
    connection = authUtil.build_connection()
    data_type = 37
    jsonResponse, jsonValues = connection.get_product_list(data_type)

    if jsonResponse:
        return product_resource.store_product_price(jsonValues)

    else:
        return {'status': "error", 'data': 'null', 'Message': "Error while retrieving product price from server"}


def get_product_by_barcode(barcode) -> dict:
    return product_resource.get_product_by_barcode(barcode)


def update_product() -> dict:
    connection = authUtil.build_connection()
    data_type = 3
    json_response, json_values = connection.get_product_list(data_type)

    if json_response:
        return product_resource.update_product(json_values)
    else:
        return {'status': "error", 'data': 'null', 'Message': "Error while retrieving product from server"}


def update_product_price() -> dict:
    connection = authUtil.build_connection()
    data_type = 37
    json_response, json_values = connection.get_product_list(data_type)
    if json_response:
        return product_resource.update_product_price(json_values)

    else:
        return {'status': "error", 'data': 'null',
                'Message': "Error while retrieving product price from SQUIZZ server"}
