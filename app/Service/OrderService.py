from app.Util import AuthUtil as authUtil
from app.Resource.OrderResource import OrderResource

order_resource = OrderResource()


def submit_order(session_key, order_details) -> dict:
    connection = authUtil.build_connection()
    squizzRep, purchaseList = connection.submit_purchase(session_key, order_details)
    if squizzRep == 'SERVER_SUCCESS':
        return order_resource.purchase(session_key, squizzRep, purchaseList)
    else:
        return {'status': "error", 'data': 'null', 'Message': "Error while sending purchase to SQUIZZ server"}


def search_history(data) -> dict:
    try:
        result = order_resource.history_order(data['session_id'], data['date_time'])
    except Exception as e:
        return {'status': "failure", 'data': 'null', 'Message': "Wrong Session, please login again"}

    return result
