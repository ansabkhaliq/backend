from app.Model.Product import Product
from app.Resource.ProductResource import ProductResource
from app.Resource.UserResource import UserResource
from app.Resource.ModelMetadataResource import ModelMetadataResource
from app.Util import AuthUtil as authUtil


def retrieve_products(customer_code="TESTDEBTOR") -> dict:
    connection = authUtil.build_connection()
    data_type = 3
    success, product_list = connection.retrieve_organisation_data(data_type, customer_code=customer_code)
    product_resource = ProductResource()
    if success:
        return product_resource.store_products(product_list)

    return {
        'status': "error",
        'data': None,
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
        'data': None,
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
                product_record.imageList = image_records

            result = {
                'status': "success",
                'message': "successfully retrieved product",
                'data': product_record.__dict__
            }

        else:
            result = {
                'status': "error",
                'data': None,
                'Message': "No data found"
            }
    except Exception as e:
        result = {
            'status': "error",
            'data': None,
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
                'data': None,
                'Message': "No data found"
            }
    except Exception as e:
        result = {
            'status': "error",
            'data': None,
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
        'data': None,
        'Message': 'Error while retrieving product from server'
    }


def update_prices() -> dict:
    connection = authUtil.build_connection()
    data_type = 37
    success, price_list = connection.retrieve_organisation_data(data_type)
    product_resource = ProductResource()

    if success:
        return product_resource.update_prices(price_list)

    return {
        'status': 'error',
        'data': None,
        'Message': "Error while retrieving product price from SQUIZZ server"
    }


def import_metadata(data) -> dict:
    username = data['Username']
    password = data['Password']
    try:
        user_resource = UserResource()
        org_id = user_resource.validate_username_password(username, password)
    except AttributeError:
        return {'status': "failure", "message": "LOGIN_ERROR"}

    if org_id is None:
        # wrong username or password
        return {'status': "failure", "message": "LOGIN_ERROR"}
    product_list = data['Products']
    errormessage = ""
    for product in product_list:
        code = product['Code']
        product_id = ProductResource.get_product_id_by_product_code(code)
        if product_id is None:
            errormessage += str(code) + ", "
            continue
        model_metadata_resource = ModelMetadataResource()
        status_code = model_metadata_resource.insert_metadata(product_id, code, str(product['ProductParameters']))
        if status_code == 1:
            errormessage += code + ", "
            continue
    if errormessage == "":
        return {"status": "success", "message": "import success"}
    else:
        return {"status": "partial success",
                "message": "product code with" + errormessage + "failed to upload, please check the product code or "
                                                                "try again"}
