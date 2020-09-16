from app.Model.OrderDetail import OrderDetail
from app.Service import OrderService as order_service
from app.Util import AuthUtil as authUtil
from flask import (
    Blueprint,
    redirect,
    request,
    jsonify,
    url_for
)

order = Blueprint('order', __name__)


@order.route('/api/purchase', methods=['post'])
def submit_purchase_order():
    if not authUtil.validate_login_session:
        return redirect(url_for('auth.login'))

    data = request.get_json(silent=True)
    session_key = data['sessionKey']
    order_details = [OrderDetail(order_detail) for order_detail in data['lines']]
    return jsonify(order_service.submit_order(session_key, order_details))


@order.route('/api/history_order', methods=['post'])
def search_history_order():
    if not authUtil.validate_login_session:
        return redirect(url_for('auth.login'))

    data = request.get_json(silent=True)
    return jsonify(order_service.search_history(data))
