from app.Util import AuthUtil as authUtil
from app.Service import ProductService as product_service
from flask import (
    Blueprint,
    redirect,
    request,
    jsonify,
    url_for,
)

product = Blueprint('product', __name__)


# Example of the API call
# http://127.0.0.1:3000/api/product?sessionKey=8A96E4EF6C4C9ECC4938A7DB816346DC&barcode=9326243001262
@product.route('/api/barcode', methods=['GET'])
def get_barcode_product():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))

    barcode = request.args.get('barcode')
    return jsonify(product_service.get_product_by_barcode(barcode))



# Example of the API call
# http://127.0.0.1:3000/api/product?sessionKey=8A96E4EF6C4C9ECC4938A7DB816346DC&productCode=01248
@product.route('/api/product', methods=['GET'])
def get_product_by_id():
    sessionKey = request.args.get('sessionKey')
    if not authUtil.validate_login_session(sessionKey):
        return redirect(url_for('auth.login'))

    productCode = request.args.get('productCode')
    return jsonify(product_service.get_product_by_product_code(productCode))


# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database
@product.route('/retrieveProducts', methods=['GET'])
def retrieve_products():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return jsonify(product_service.retrieve_products())


# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the latest product prices from SQUIZZ platform and updating the table in the local database
@product.route('/retrievePrices', methods=['GET'])
def retrieve_prices():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return jsonify(product_service.retrieve_prices())


# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the product update from SQUIZZ platform and updating the table in the local database
@product.route('/updateProducts', methods=['GET'])
def update_products():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))

    return jsonify(product_service.update_products())
    

# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the latest product prices from SQUIZZ platform and updating the table in the local database
@product.route('/updatePrices', methods=['GET'])
def update_product_price():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return jsonify(product_service.update_prices())
