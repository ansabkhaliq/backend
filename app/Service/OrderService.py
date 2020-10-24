from app.Util import AuthUtil as authUtil
from app.Resource.OrderResource import OrderResource


def submit_order(session_key, order_details) -> dict:
    connection = authUtil.build_connection()
    result_code, order = connection.submit_purchase(session_key, order_details)
    
    if result_code == 'SERVER_SUCCESS':
        order_resource = OrderResource()
        return order_resource.store_purchase(session_key, result_code, order)
    
    return {
        'status': "error",
        'data': None,
        'Message': "Error while sending purchase to SQUIZZ server"
    }


def get_order_history(session_id) -> dict:
    try:
        order_resource = OrderResource()
        result = order_resource.get_order_history(session_id)
    except Exception as e:
        result = {
            'status': 'failure',
            'data': None,
            'message': "Invalid session, please login again"
        }

    return result


def save_order(customer_id, delivery_addr_id, billing_addr_id, product_dict):
    pass
