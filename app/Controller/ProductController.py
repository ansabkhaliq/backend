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

@product.route('/api/price', methods=['POST'])
def get_barcode_product():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))

    data = request.get_json(silent=True)
    barcode = data.get('barcode')
    return jsonify(product_service.get_product_by_barcode(barcode))


# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database
@product.route('/retrieveproduct', methods=['GET'])
def retrieve_product():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return jsonify(product_service.retrieve_product())

# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the latest product prices from SQUIZZ platform and updating the table in the local database
@product.route('/retrieveprice', methods=['GET'])
def retrieve_product_price():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return product_service.retrieve_product_price()

# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the product update from SQUIZZ platform and updating the table in the local database
@product.route('/updateproduct', methods=['GET'])
def update_product():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))

    return jsonify(product_service.update_product())

# This method is not called from the front end. These are supposed to be called by the Postman or another similar tool that
# allow you to make calls to the REST API.
# This method is repsonbile for getting the latest product prices from SQUIZZ platform and updating the table in the local database
@product.route('/updateprice', methods=['GET'])
def update_product_price():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return jsonify(product_service.update_product_price())
