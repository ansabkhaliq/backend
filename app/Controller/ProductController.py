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


@product.route('/retrieveproduct', methods=['GET'])
def retrieve_product():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return jsonify(product_service.retrieve_product())


@product.route('/retrieveprice', methods=['GET'])
def retrieve_product_price():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return product_service.retrieve_product_price()



@product.route('/api/price', methods=['POST'])
def get_barcode_product():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))

    data = request.get_json(silent=True)
    barcode = data.get('barcode')
    return jsonify(product_service.get_barcode_value(barcode))



@product.route('/updateproduct', methods=['GET'])
def update_product():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))

    return jsonify(product_service.update_product())


@product.route('/updateprice', methods=['GET'])
def update_product_price():
    if not authUtil.validate_login_session():
        return redirect(url_for('auth.login'))
    return jsonify(product_service.update_product_price())
