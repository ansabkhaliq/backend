from app.Util import AuthUtil as authUtil
from app.Resource.OrderResource import OrderResource

order_resource = OrderResource()


def submit_order(session_key, order_details) -> dict:
    connection = authUtil.build_connection()
    result_code, order = connection.submit_purchase(session_key, order_details)
    
    if result_code == 'SERVER_SUCCESS':
        return order_resource.store_purchase(session_key, result_code, order)
    
    return {
        'status': "error",
        'data': 'null',
        'Message': "Error while sending purchase to SQUIZZ server"
    }


def get_order_history(session_id) -> dict:
    try:
        result = order_resource.get_order_history(session_id)
    except Exception as e:
        result = {
            'status': 'failure',
            'data': 'null',
            'message': "Invalid session, please login again"
        }

    return result
