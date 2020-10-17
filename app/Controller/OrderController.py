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

from flask_cors import cross_origin


@order.route('/api/purchase', methods=['POST'])
@cross_origin()
def submit_purchase_order():
    if not authUtil.validate_login_session:
        return redirect(url_for('auth.login'))

    data = request.get_json(silent=True)
    session_key = data['sessionKey']
    order_details = [OrderDetail(line) for line in data['lines']]
    return jsonify(order_service.submit_order(session_key, order_details))


@order.route('/api/history', methods=['GET', 'POST'])
@cross_origin()
def retrieve_order_history():
    if not authUtil.validate_login_session:
        return redirect(url_for('auth.login'))

    session_id = request.args.get('session_id')
    return jsonify(order_service.get_order_history(session_id))
