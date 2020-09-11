from app.Controller import UserController as auth
from Resource.OrderResource import OrderResource
from Resource.ProductResource import ProductResource
from Resource.UserResource import UserResource
from flask import (
    Blueprint, 
    redirect, 
    request, 
    jsonify, 
    url_for, 
)

# Configure Flask application
main = Blueprint('main', __name__)

# Initialise database resource objects
order_resource = OrderResource()
product_resource = ProductResource()
user_resource = UserResource()


# -- Application routes



@main.route('/api/purchase', methods=['post'])
def submit_purchase_order():
    if not auth.validate_login_session:
        return redirect(url_for('auth.login'))
    connection = auth.build_connection()
    data = request.get_json(silent=True)
    squizzRep, purchaseList = connection.submit_purchase(data)
    if squizzRep == 'SERVER_SUCCESS':
        result = order_resource.purchase(data["sessionKey"], squizzRep, purchaseList)
        return jsonify(result)
    else:
        result = {'status': "error", 'data': 'null', 'Message': "Error while sending purchase to SQUIZZ server"}
        return jsonify(result)


@main.route('/api/history_order', methods=['post'])
def search_history_order():
    if not auth.validate_login_session:
        return redirect(url_for('auth.login'))
    connection = auth.build_connection()
    data = request.get_json(silent=True)
    try:
        result = order_resource.history_order(data['session_id'], data['date_time'])
    except Exception as e:
        result = {'status': "failure", 'data': 'null', 'Message': "Wrong Session, please login again"}
        return jsonify(result)
    return jsonify(result)
