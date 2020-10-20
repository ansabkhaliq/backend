import json
import requests
from datetime import datetime

s = requests.Session()
squizz_sessions = []
base_url = "http://127.0.0.1:5000/"
null = None


def test_login():
    url = 'api/login'
    headers = {"Content-Type": "application/json"}

    data = {"username": "user1", "password": "123456789"}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "failure"

    data = {"username": "user1", "password": "squizz"}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"
    content = json_response['data']
    squizz_sessions.append(content['session_id'])
    # print(json_response['session_id'])


def test_barcode_search():
    if len(squizz_sessions) == 0:
        test_login()
    url = 'api/barcode'
    para = '?sessionKey=' + squizz_sessions[0] + '&barcode=933044000895'
    response = s.get(base_url + url + para)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"
    para1 = '?sessionKey=' + squizz_sessions[0] + '&barcode=123'
    response = s.get(base_url + url + para1)
    json_response = json.loads(response.text)
    assert json_response['status'] == "error"


# CANT USE THIS AS IT STORES DATA IN DATABASE
def test_product():
    if len(squizz_sessions) == 0:
        test_login()
    base_url = "http://127.0.0.1:5000/"
    url = 'api/product'
    para = '?sessionKey=' + squizz_sessions[0] + '&productCode=00089'
    response = s.get(base_url + url + para)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"
    para = '?sessionKey=' + squizz_sessions[0] + '&productCode=-1'
    response = s.get(base_url + url + para)
    json_response = json.loads(response.text)
    assert json_response['status'] == "error"


def test_history_order():
    if len(squizz_sessions) == 0:
        test_login()
    url = 'api/history'
    response = s.post(base_url + url)
    json_response = json.loads(response.text)
    assert json_response['status'] == "error"
    para = '?session_id=' + squizz_sessions[0]
    response = s.get(base_url + url + para)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"


def test_submit_order():
    if len(squizz_sessions) == 0:
        test_login()
    url = 'api/purchase'
    headers = {"Content-Type": "application/json"}
    order_details = [
        {
            "keyProductId": "21479231996639",
            "productName": "test",
            "quantity": "2",
            "unitPrice": "1.38",
            "totalPrice": "2.76",
            "priceTotalIncTax": "0.00",
            "priceTotalExTax": "0.00",
            "productCode": "21479231996639",
            "productId": "20",
        }
    ]
    data = {'lines': order_details, 'sessionKey': squizz_sessions[0]}

    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "error"
    data = {'lines': order_details}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "failure"

    data = {}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "failure"

    data = {'sessionKey': squizz_sessions[0]}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "failure"

    order_details = [{
        "barcode": "9326243001224",
        "depth": 0,
        "height": 0,
        "id": 5,
        "keyProductID": "21479231981826",
        "lineType": "PRODUCT",
        "price": 8.23,
        "priceTotalExTax": 8.23,
        "productCode": "01224",
        "productName": "Tarpaulin 240cm x 300cm (8' x 10')",
        "quantity": 1,
        "stockLowQuantity": 0,
        "stockQuantity": 0,
        "totalPrice": 8.23,
        "unitPrice": 8.23,
        "volume": 0,
        "weight": 0,
        "width": 0}]
    data = {'lines': order_details, 'sessionKey': squizz_sessions[0]}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"


def test_logout():
    url = 'api/logout'
    response = s.get(base_url + url)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"
    squizz_sessions.pop()
