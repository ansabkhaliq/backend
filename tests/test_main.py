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

    order_details = [{"averageCost": null,
                      "barcode": "9326243001224",
                      "barcodeInner": null,
                      "brand": null,
                      "categoryList": null,
                      "depth": 0,
                      "description1": null,
                      "description2": null,
                      "description3": null,
                      "description4": null,
                      "drop": null,
                      "height": 0,
                      "id": 5,
                      "imageList": {"fileName": "49867",
                                    "id": 723,
                                    "is3DModelType": "N",
                                    "largeImageLocation": "https://attachments.pjsas.com.au/products/images_large/49867.jpg",
                                    "mediumImageLocation": "https://attachments.pjsas.com.au/products/images_medium/49867.jpg",
                                    "productId": 5,
                                    "smallImageLocation": "https://attachments.pjsas.com.au/products/images_small/49867.jpg",
                                    "threeDModelLocation": null},
                      "internalID": null,
                      "isKitted": null,
                      "isPriceTaxInclusive": null,
                      "keyProductID": "21479231981826",
                      "keySellUnitID": null,
                      "keyTaxcodeID": null,
                      "kitProductsSetPrice": null,
                      "lineType": "PRODUCT",
                      "name": null,
                      "packQuantity": null,
                      "price": 8.23,
                      "priceList": null,
                      "priceTotalExTax": 8.23,
                      "productCode": "01224",
                      "productCondition": null,
                      "productName": "Tarpaulin 240cm x 300cm (8' x 10')",
                      "productSearchCode": null,
                      "quantity": 1,
                      "sellUnits": null,
                      "sellUnitsIdList": null,
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
