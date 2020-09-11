from app.Util import AuthUtil as authUtil
from flask import (
    Blueprint,
    redirect,
    request,
    jsonify,
    url_for,
)
from app.Service import OrderService as order_service

order = Blueprint('order', __name__)

@order.route('/api/purchase', methods=['post'])
def submit_purchase_order():
    if not authUtil.validate_login_session:
        return redirect(url_for('auth.login'))

    data = request.get_json(silent=True)
    return jsonify(order_service.submit_order(data))



@order.route('/api/history_order', methods=['post'])
def search_history_order():
    if not authUtil.validate_login_session:
        return redirect(url_for('auth.login'))

    data = request.get_json(silent=True)
    return jsonify(order_service.search_history(data))

