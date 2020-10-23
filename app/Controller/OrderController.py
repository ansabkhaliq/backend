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
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
order = Blueprint('order', __name__)


@order.route('/api/purchase', methods=['POST'])
def submit_purchase_order():

    data = request.get_json(silent=True)
    if not (data.__contains__('sessionKey') and data.__contains__('lines')):
        return jsonify({
            'status': "failure",
            'data': 'null',
            'Message': "Invalid data"
        })
    session_key = data['sessionKey']
    order_details = [OrderDetail(line) for line in data['lines']]
    return jsonify(order_service.submit_order(session_key, order_details))


@order.route('/api/history', methods=['GET', 'POST'])
def retrieve_order_history():

    session_id = request.args.get('session_id')
    return jsonify(order_service.get_order_history(session_id))
