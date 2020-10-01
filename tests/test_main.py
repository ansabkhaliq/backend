import json
import requests
from datetime import datetime

s = requests.Session()
squizz_sessions = []
base_url = "http://127.0.0.1:5000/"


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
    url = 'api/history_order'
    headers = {"Content-Type": "application/json"}
    now = datetime.now()
    date = now.strftime("%Y/%m/%d %H:%M:%S")
    data = {'date_time': date}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "failure"

    data = {'session_id': squizz_sessions[0], 'date_time': date}
    response = s.post(base_url + url, data=json.dumps(data), headers=headers)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"


def test_logout():
    url = 'api/logout'
    response = s.get(base_url + url)
    json_response = json.loads(response.text)
    assert json_response['status'] == "success"
    squizz_sessions.pop()
